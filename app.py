"""
Main code for Flask Server.
Utilizes authlib, OAuth, and Google for login.
Handles livestreaming through opencv2.
Stores environment/secret variables with os.
"""
from flask import Flask, render_template, Response, url_for, session, redirect
import cv2
import os
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
camera = cv2.VideoCapture(0)


def gen_frames():
    """
    Creates a livestream through continuously taking pictures and constantly updating it.
    This way it operates as a video being livestreamed, albeit with no audio.
    """
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@app.route('/video_feed')
def video_feed():
    """
    The livestream link from host through ngrok.
    """
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def landing():
    """
    The Landing screen to login with.
    """
    user = session.get('user')
    return render_template('landing.html', user=user)


@app.route('/login/')
def login():
    """
    Sends you to login through google.
    """
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/home/')
def home():
    """
    Obtains user and makes sure they're logged in before sending them to the home page.
    Otherwise redirected to landing screen.
    """
    user = session.get('user')
    if not user:
        return redirect('/')
    else:
        return render_template('home.html', user=user)


@app.route('/auth')
def auth():
    """
    Obtains a token and creates a user profile from the google login.
    Then redirects them to the home page.
    """
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect('/home/')


@app.route('/logout')
def logout():
    """
    Logs out the user.
    """
    session.pop('user', None)
    return redirect('/')


@app.route('/staticvideos/')
def staticvideos():
    """
    Obtains user and makes sure they're logged in before sending them to the static videos page.
    Otherwise redirected to landing screen.
    """
    user = session.get('user')
    if not user:
        return redirect('/')
    else:
        return render_template('staticvideo.html', user=user)


@app.route('/livestream')
def livestreaming():
    """
    Obtains user and makes sure they're logged in before sending them to the livestream page.
    Otherwise redirected to landing screen.
    """
    user = session.get('user')
    if not user:
        return redirect('/')
    else:
        return render_template('livestream.html', user=user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", threaded=True)
