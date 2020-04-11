from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import functools
from werkzeug.security import check_password_hash, generate_password_hash

from dem3_multi.db import get_db, get_user, get_usernames, select, insert

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
        password = generate_password_hash(password)

        error = None
        if username_exists(username):
            error = f"User {username} already exists."

        if not error:
            insert('users', values=[username, password]) #! add_user(username, password)
            return redirect(url_for('auth.login'))
        
        flash(error)

    usernames = get_usernames()

    return render_template('auth/register.html', usernames=usernames)

def username_exists(username:str) -> bool:
    db = get_db()

    query = "SELECT username FROM users " \
        "WHERE username = ?"
    
    return bool(db.execute(query, (username,)).fetchone())
        
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)

        error = None
        if not user:
            error = "User doesn't exist."
        elif not check_password_hash(user.password, password):
            error = "Password is incorrect."
        
        if not error:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for("dem3.dashboard"))
        
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('dem3.index'))

@bp.before_app_request
def load_logged_in_user():
    """
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view