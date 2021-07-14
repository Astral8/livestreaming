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
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def landing():
    user = session.get('user')
    return render_template('landing.html', user=user)


@app.route('/login/')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/home/')
def home():
    user = session.get('user')
    if not user:
        return redirect('/')
    else:
        return render_template('home.html', user=user)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect('/home/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/staticvideos/')
def staticvideos():
    user = session.get('user')
    if not user:
        return redirect('/')
    else:
        return render_template('staticvideo.html', user=user)


@app.route('/livestream')
def livestreaming():
    user = session.get('user')
    if not user:
        return redirect('/')
    else:
        return render_template('livestream.html', user=user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", threaded=True)
