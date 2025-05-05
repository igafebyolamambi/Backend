from flask import Flask, request
from app.config.middleware import checkLogin
from app.controllers import home, misc, user, api, history
import os

app = Flask(__name__)

# ---------------------- START LOGIN -----------------------------
@app.route("/login")
def login_index():
    return misc.index()

@app.route("/doLogin", methods=['POST'])
def doLogin():
    return misc.doLogin(request.form)

@app.route("/logout")
def logout():
    return misc.logout()

@app.route("/home")
def home_index():
    return home.index()

@app.route("/")
@checkLogin
def index():
    return home.index()
# ---------------------- END LOGIN -----------------------------

# ---------------------- START USER -----------------------------
@app.route("/users")
@checkLogin
def user_index():
    return user.index() 

@app.route("/users/create")
@checkLogin
def user_create():
    return user.create() 

@app.route("/users/<int:id>/edit")
@checkLogin
def user_edit(id):
    return user.edit(id)

@app.route("/users/store", methods=['POST'])
@checkLogin
def user_store():
    return user.store(request.form)

@app.route("/users/<int:id>/update", methods=['POST'])
@checkLogin
def users_update(id):
    return user.update(request, id)

@app.route("/users/<int:id>/delete")
@checkLogin
def user_delete(id):
    return user.delete(id)
# ---------------------- END USER -----------------------------

# ---------------------- START HISTORY -----------------------------
@app.route("/history")
@checkLogin
def history_index():
    return history.index()
# ---------------------- END HISTORY -----------------------------

# ---------------------- START API -----------------------------
@app.route("/api-login", methods=['POST'])
def user_login():
    return api.login()

@app.route("/api-register", methods=['POST'])
def user_register():
    return api.register()

@app.route("/api-predict", methods=['POST'])
def user_predict():
    return api.predict()

@app.route('/uploads/<filename>')
def user_uploaded_file(filename):
    return api.uploaded_file(filename)

@app.route("/api-history")
def user_history():
    return api.history()
# ---------------------- END HISTORY -----------------------------

app.secret_key = '1234567890'
app.config['SESSION_TYPE'] = 'filesystem'

@app.context_processor
def inject_stage_and_region():
    return dict(APP_NAME=os.environ.get("APP_NAME"),
        APP_AUTHOR=os.environ.get("APP_AUTHOR"),
        APP_TITLE=os.environ.get("APP_TITLE"),
        APP_LOGO=os.environ.get("APP_LOGO"))

if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=5595)