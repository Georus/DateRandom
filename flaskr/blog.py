from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
def index():
    db = get_db()
    shows = db.execute(
        '''
        SELECT activities.id, name, category, username, author_id
        FROM activities JOIN user ON activities.author_id = user.id
        WHERE category = 'shows';
        '''
    ).fetchall()
    dinners = db.execute(
        '''
        SELECT activities.id, name, category, username, author_id
        FROM activities JOIN user ON activities.author_id = user.id
        WHERE category = 'dinners';
        '''
    ).fetchall()
    miscs = db.execute(
        '''
        SELECT activities.id, name, category, username, author_id
        FROM activities JOIN user ON activities.author_id = user.id
        WHERE category = 'misc';
        '''
    ).fetchall()
    sexys = db.execute(
        '''
        SELECT activities.id, name, category, username, author_id
        FROM activities JOIN user ON activities.author_id = user.id
        WHERE category = 'sexy';
        '''
    ).fetchall()
    showstemp = {'hdr': 'Shows', 'list' : shows}
    dinnerstemp = {'hdr': 'Dinners', 'list' : dinners}
    miscstemp = {'hdr': 'Miscellaneous', 'list' : miscs}
    sexystemp = {'hdr': 'You know ;)', 'list' : sexys}
    
    columns = [showstemp, dinnerstemp, miscstemp, sexystemp]
    return render_template('blog/index.html', columns=columns)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        actname = request.form['name']
        desc = request.form['description']
        cat = request.form['category']
        error = None

        if not actname:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO activities (name, description, category, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (actname, desc, cat, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
         '''
        SELECT activities.id, name, description, username, author_id
        FROM activities JOIN user ON activities.author_id = user.id
        WHERE activities.id = ?;
        ''',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    act = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE activities SET name = ?, description = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', act=act)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
