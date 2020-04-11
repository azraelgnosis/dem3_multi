from flask import (
        Blueprint, g, redirect, render_template, url_for
    )
import functools

from dem3_multi.db import get_db, get_tables, get_table, select

bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_privileges(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user and 'admin' in g.user.roles:
            return view(**kwargs)
        return redirect(url_for('auth.login'))
    
    return wrapped_view

@bp.route("/")
@admin_privileges
def portal():
    return "Administrative Portal"

@bp.route("/tables/")
def tables():
    tables = get_tables()

    return render_template("admin/tables.html", tables=tables)

@bp.route("/tables/<string:name>")
def table(name):
    table = get_table(name)

    return render_template("admin/table.html", table=table)