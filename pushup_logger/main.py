from flask import Blueprint, flash, render_template,redirect, url_for,request
from flask_login import login_required, current_user
from .models import User, Workout
from . import db

main = Blueprint('main', __name__)

# homepage
@main.route('/')
def index():
    return render_template('index.html')

#user profile
@main.route('/profile')
@login_required
def profile():
    page = request.args.get('page', 1, type = int)
    workouts = Workout.query.filter_by(author = current_user).paginate(page=page,per_page = 3)
    return render_template('profile.html',name=current_user.name, workouts = workouts)

#add workout
@main.route('/add_workout')
@login_required
def add_workout():
    return render_template('add_workout.html')

@main.route('/add_workout',methods = ['POST'])
@login_required
def add_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')

    workout = Workout(pushups = pushups,comment = comment, author = current_user)
    db.session.add(workout)
    db.session.commit()
    
    return redirect(url_for('main.profile'))

#edit workout
@main.route('/workout/<int:workout_id>/update',methods = ['GET','POST'])
@login_required
def edit_workout(workout_id):
    workout = Workout.query.filter_by(id = workout_id).first_or_404()
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        return redirect(url_for('main.profile'))
    
    return render_template('edit_workout.html',workout = workout)

#delete workout
@main.route('/workout/<int:workout_id>/delete',methods = ['GET','POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.filter_by(id = workout_id).first_or_404()
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.profile'))