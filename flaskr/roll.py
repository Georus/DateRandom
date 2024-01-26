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
        WHERE category = 'shows'
        ORDER by RANDOM()
        LIMIT 1;
        '''
    ).fetchone()

    dinner = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'dinners'
        ORDER by RANDOM()
        LIMIT 1;
        '''
    ).fetchone()
    misc = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'misc'
        ORDER by RANDOM()
        LIMIT 1;
        '''
    ).fetchone()
    sexy = db.execute(
        '''
        SELECT name, description, category 
        FROM activities
        WHERE category = 'sexy'
        ORDER by RANDOM()
        LIMIT 1;
        '''
    ).fetchone()

    
    showstemp = {'hdr': 'Shows', 'img': 'tv.svg', 'list' : show}
    dinnerstemp = {'hdr': 'Dinners','img': 'noodles.svg', 'list' : dinner}
    miscstemp = {'hdr': 'Miscellaneous', 'img': 'calendar.svg', 'list' : misc}
    sexystemp = {'hdr': 'You know ;)', 'img': 'fire.svg', 'list' : sexy}
    
    acts = [showstemp, dinnerstemp, miscstemp, sexystemp]

    return render_template('roll/index.html', acts=acts)
    
    
    
