"""
Flask backend for the production web application outage lab.

Author:
    Naftali Wodinsky

Date:
    July 27, 2026

Purpose:
    Runs the internal backend application used during the outage
    investigation. Nginx accepts user requests on TCP port 80 and
    forwards them to this application on 127.0.0.1:5050.

Usage:
    Install Flask:

        python -m pip install flask

    Start the application:

        python internal_web_app.py

    Test the backend directly:

        curl http://127.0.0.1:5050

The application listens only on the local loopback interface and is
intended to be reached through the Nginx reverse proxy.
"""

from datetime import datetime, timezone

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    """Display the internal application status page."""
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
