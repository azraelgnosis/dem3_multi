from flask import (
    Blueprint, render_template
)

from dem3_multi.db import select
from dem3_multi.data import mapping, get_game_data, get_game_datum

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

@bp.route('/<string:stats_type>/')
def stats(stats_type):
    data = get_game_data(stats_type)
    return render_template(f'stats.html', data=data, stats_type=stats_type)

@bp.route('/<string:stats_type>/<string:stat_name>')
def stat(stats_type, stat_name):
    datum = get_game_datum(stats_type, stat_name)
    template = mapping.get(stats_type)['subtype']
    return render_template(f'{template}.html', datum=datum)