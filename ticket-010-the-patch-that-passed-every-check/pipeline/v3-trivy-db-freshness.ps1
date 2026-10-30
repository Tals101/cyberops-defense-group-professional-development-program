function Test-TrivyDbFreshness {
    param(
        [Parameter(Mandatory = $true)]
        [string]$VersionText,

        [datetime]$NowUtc = [datetime]::UtcNow,

        [double]$MaximumAgeHours = 48
    )

    try {
        if (-not $VersionText.Contains("Vulnerability DB:")) {
            throw "Vulnerability DB metadata missing."
        }

        $section = $VersionText.Substring(
            $VersionText.IndexOf("Vulnerability DB:")
        )

        $bundleIndex = $section.IndexOf("Check Bundle:")
        if ($bundleIndex -ge 0) {
            $section = $section.Substring(0, $bundleIndex)
        }

        $timestamps = @{}

        foreach ($field in @("UpdatedAt", "NextUpdate", "DownloadedAt")) {

            $pattern = '(?m)^\s*' +
                [regex]::Escape($field) +
                ':\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'

            $match = [regex]::Match($section, $pattern)

            if (-not $match.Success) {
                throw "Missing timestamp: $field"
            }

            $styles = (
                [Globalization.DateTimeStyles]::AssumeUniversal -bor
                [Globalization.DateTimeStyles]::AdjustToUniversal
            )

            $timestamps[$field] = [datetime]::ParseExact(
                $match.Groups[1].Value,
                "yyyy-MM-dd HH:mm:ss",
                [Globalization.CultureInfo]::InvariantCulture,
                $styles
            )
        }

        $updated = $timestamps["UpdatedAt"]
        $nextUpdate = $timestamps["NextUpdate"]
        $downloaded = $timestamps["DownloadedAt"]

        $ageHours = ($NowUtc - $updated).TotalHours

        $approved = (
            $ageHours -ge -0.167 -and
            $ageHours -le $MaximumAgeHours -and
            $nextUpdate -gt $NowUtc -and
            $nextUpdate -gt $updated -and
            $downloaded -le $NowUtc.AddMinutes(10) -and
            $downloaded -ge $updated.AddMinutes(-10)
        )

        $reason = if ($approved) {
            "Database meets freshness requirements."
        } else {
            "Database timestamps violate freshness requirements."
        }

        return [PSCustomObject]@{
            Approved = [bool]$approved
            Reason = $reason
            AgeHours = [math]::Round($ageHours, 2)
        }
    }
    catch {
        return [PSCustomObject]@{
            Approved = $false
            Reason = "Invalid metadata: $($_.Exception.Message)"
            AgeHours = $null
        }
    }
}
