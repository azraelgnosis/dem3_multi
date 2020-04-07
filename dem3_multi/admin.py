from flask import (
        Blueprint, g, redirect, render_template, url_for
    )
import functools

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/")
@admin_privileges
def portal():
    return "Administrative Portal"


def admin_privileges(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user and 'admin' in g.user.roles:
            return view(**kwargs)
        return redirect(url_for('auth.login'))
    
    return wrapped_view