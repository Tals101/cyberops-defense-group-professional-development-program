"""
Purpose:
    Provides the Flask backend used to reproduce and investigate the
    production web application outage scenario.

Author:
    Harold Wodinsky

Date:
    July 27, 2026

Usage:
    1. Install Flask:
       python -m pip install flask

    2. Run the application:
       python internal_web_app.py

    3. Test the backend locally:
       curl http://127.0.0.1:5050

The application listens only on 127.0.0.1:5050 and is intended to be
accessed through the Nginx reverse proxy.
"""

from datetime import datetime, timezone

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    """Return the internal application status page."""
    current_time = datetime.now(timezone.utc).isoformat()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Internal Company Portal</title>
    </head>
    <body>
        <h1>Internal Company Web Application</h1>
        <p>Status: Operational</p>
        <p>Backend application is responding normally.</p>
        <p>Server time: {current_time}</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050)
