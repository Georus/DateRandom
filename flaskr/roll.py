from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('roll', __name__)

@bp.route('/')
def index():
    db = get_db()
    act = db.execute(
        '''
        SELECT name, description, category 
        FROM activities;
        '''
    ).fetchone()
    return render_template('roll/index.html', act=act)
