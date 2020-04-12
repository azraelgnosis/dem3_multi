from flask import (
    Blueprint, render_template
)

from dem3_multi.db import select
from dem3_multi.data import get_game_data, get_game_datum

bp = Blueprint('dem3', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@bp.route('/games')
def games():
    games = select('games')
    return render_template('games.html', games=games)

@bp.route('/games/<int:id>')
def game(id:int):
    game = select('games', id=id)
    return render_template('game.html', game=game)

@bp.route('/policies')
def policies():
    policies = get_game_data('policies') #policies = get_policies()
    return render_template('policies.html', policies=policies)

@bp.route('/policies/<string:policy_name>')
def policy(policy_name:str):
    policy = get_game_datum('policies', policy_name) # policy = get_policy(policy_name)
    return render_template('policy.html', policy=policy)

@bp.route('/situations/')
def situations():
    situations = get_game_data('situations')
    return render_template('situations.html', situations=situations)

@bp.route('/situations/<string:name>')
def situation(name:str):
    situation = get_game_datum('situations', name)
    return render_template('situation.html', situaiton=situation)