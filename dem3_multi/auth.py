from flask import (
    Blueprint, render_template, request
)

from dem3_multi.data import get_db, get_usernames

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    usernames = get_usernames()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        

    return render_template('auth.html', usernames=usernames)

def username_exists(username:str) -> bool:
    db = get_db()

    sql_check_player = "SELECT * FROM players" \
        "WHERE username == ?"
    
    return bool(db.execute(sql_check_player, username))
        


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        pass
    return render_template('auth.html') # return render_template('auth/login.html')

def logout(): ...