from flask import (
    Blueprint, render_template
)

from dem3_multi.data import get_games, get_game, get_policies

bp = Blueprint('dem3', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@bp.route('/games')
def games():
    games = get_games()
    return render_template('games.html', games= games)

@bp.route('/games/<int:id>')
def game(id:int):
    """
    """
    game = get_game(id)

    return render_template('game.html', game=game)

@bp.route('/policies')
def policies():
    """
    """

    policies = get_policies()

    return render_template('policies.html', policies=policies)