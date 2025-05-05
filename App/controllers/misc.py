from flask import render_template, redirect, session, url_for, flash
from app.models.User import *
import bcrypt

def index():
    if "user" in session:
        return redirect(url_for("index"))
    else:
        return render_template('pages/login.html', segment='login')

def doLogin(data):
    user = User.get_by_username(data['username'])
    if user == None:
        flash('Username tidak sesuai.!', 'danger')
        return redirect(url_for('login_index'))
    if user == False:
        flash('Terjadi kesalahan, silahkan cek console.!', 'danger')
        return redirect(url_for('login_index'))
    if bcrypt.checkpw(data['password'].encode('utf8'), user['password'].encode('utf8')):
        if user['roles'] == 'admin':
            session['user'] = user
            return redirect(url_for("index"))
        else:
            flash('Hanya admin yang bisa akses halaman ini.!', 'danger')
            return redirect(url_for('login_index'))
    else:
        flash('Password tidak sesuai.!', 'danger')
        return redirect(url_for('login_index'))

def logout():
	if "user" in session:
		session.pop("user", None)
	return redirect(url_for("login_index"))