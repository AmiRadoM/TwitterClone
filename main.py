# main.py - the script that starts the web app

from app import create_app

app = create_app()

app.run(host="0.0.0.0", port=5050, debug=True)