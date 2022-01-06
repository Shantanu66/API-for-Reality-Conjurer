# Download the trained Model here:
https://www.mediafire.com/file/nhn4jz0v6ivlizc/test.h5/file

# Steps to run the server

Open cmd and go to the server path and run these commands to set the server to a local host and run it locally
(Try cmder:a better alternative to windows cmd line/powershell)

    set FLASK_APP=flask_api.py
    set FLASK_ENV=development
    flask run --host=192.168.1.3

After this run the main Reality conjurer app using your Flutter emulator(Clone that repository first)
