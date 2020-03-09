from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        pass

    return render_template('auth/register.html')

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')

def logout(): ...