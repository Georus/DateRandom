from flask import (Blueprint, render_template)
from flaskr.db import get_db

bp = Blueprint('roll', __name__, url_prefix='/roll')

@bp.route('/')
def index():
    db = get_db()
    show = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'shows';
        '''
    ).fetchone()
    dinner = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'dinners';
        '''
    ).fetchone()
    misc = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'misc';
        '''
    ).fetchone()
    sexy = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'sexy';
        '''
    ).fetchone()

    acts = [show, dinner, misc, sexy]
    headers = ['Shows', 'Dinners', 'Miscellaneous', 'You know ;)']
    dictacts = []
    
    for i in range(4):
        if acts[i] != None:
            dictacts.append(dict(acts[i]))
            dictacts[i]['header'] = headers[i]
    
    return render_template('roll/index.html', acts=dictacts)
    
    
    
