import os
import re
import random
from random import randrange
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)

from werkzeug.exceptions import abort

from mygdr.db import get_db

bp = Blueprint('gdr', __name__)

import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('gdr.index'))
        
        return view(**kwargs)
    
    return wrapped_view

def shuffle_questions(questions):
    if len(questions) == len(session["used_questions"]):
        session["used_questions"].clear()

    results = []
    for q in questions:
        if q["id"] not in session["used_questions"]:
            results.append(q)

    return results
        

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            db.execute(
                "INSERT INTO user (username) VALUES (?)",
                (username,),
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

        if error is not None:
            flash(error)
        else:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('gdr.index'))

    session["used_questions"] = []
    session['ncorr'] = 0
    return render_template('gdr/index.html')

def get_list_by_col(items, col):
    results = []
    for i in items:
        results.append(i[col])
    return results

@bp.route('/quiz', methods=('GET', 'POST'))
@login_required
def quiz():
    db = get_db()

    if request.method == 'POST':
        answer = int(request.form['answer'])
        error = None
        question = db.execute(
            'SELECT * FROM questions WHERE id = ?', (session['question_id'],)
        ).fetchone()        
        
        if answer==question["answer"]: session['ncorr'] += 1

        # if session['ncorr'] == 3:
        #     db.execute(
        #         'UPDATE user SET rewards_id = ? WHERE username = ?', (rewards_id, g.user["username"])
        #     )

        return redirect(url_for('gdr.quiz'))
        
    questions = db.execute(
        'SELECT * FROM questions'
    ).fetchall()
    # remove repeated
    questions = shuffle_questions(questions)
    question = random.choice(questions)
    session['question_id'] = question["id"]
    session["used_questions"].append(question["id"])

    return render_template('gdr/quiz.html', question=question)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
	).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gdr.index'))
        
