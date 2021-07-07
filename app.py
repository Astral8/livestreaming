from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template('login.html')


@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/staticvideos/')
def staticvideos():
    return render_template('staticvideo.html')


@app.route('/livestream')
def livestreaming():
    return render_template('livestream.html')

if __name__ == '__main__':
    app.run(debug=True)
