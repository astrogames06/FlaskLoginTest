from flask import *
from authlib.integrations.flask_client import *
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

oauth = OAuth(app)

# Google
google = oauth.register(
    name="google",
    client_id="891122457017-ff7ddja8onim0vsrir82l5khqvs2begq.apps.googleusercontent.com",
    client_secret=os.environ.get("google_client_secret"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"},
)

# GitHub
github = oauth.register(
    name="github",
    client_id="Ov23liAPayHFycWA08oW",
    client_secret=os.environ.get("github_client_secret"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

@app.route("/")
def index():
    # user = session.get("user") or {}
    return render_template("index.html")

@app.route("/login/google")
def login_google():
    return google.authorize_redirect(url_for("auth_google", _external=True))

@app.route("/login/github")
def login_github():
    return github.authorize_redirect(url_for("auth_github", _external=True))

@app.route("/auth/google")
def auth_google():
    token = google.authorize_access_token()
    user = google.get("userinfo").json()
    session["user"] = user
    return redirect("/")

@app.route("/auth/github")
def auth_github():
    token = github.authorize_access_token()
    user = github.get("user").json()
    session["user"] = user
    return redirect("/")

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), debug=True)