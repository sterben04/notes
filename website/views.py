from flask import Blueprint, request, flash, jsonify
from flask.helpers import flash
from flask.templating import render_template
from flask_login import login_required, current_user   
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')
    return render_template("index.html", user=current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)  #convert to python dictionary
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})