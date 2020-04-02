from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from dem3_multi.data import get_db, get_usernames

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
        password = generate_password_hash(password)

        db = get_db()

        query = "INSERT INTO players (username, password) VALUES (?, ?)"
        db.execute(query, (username, password))
        db.commit()

        return redirect(url_for('auth.login'))

    usernames = get_usernames()

    return render_template('auth/register.html', usernames=usernames)

def username_exists(username:str) -> bool:
    db = get_db()

    sql_check_player = "SELECT * FROM players" \
        "WHERE username == ?"
    
    return bool(db.execute(sql_check_player, username))
        


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        pass
    return render_template('auth/login.html') # return render_template('auth/login.html')

def logout(): ...