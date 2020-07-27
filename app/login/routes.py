import json

from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.login import bp
from app.login.forms import LoginForm
from app.login.helpers import start_user_session, end_user_sessions
from app.login.models import User, create_default_users


default_admin_page = 'default.index'
default_user_page = 'default.index'


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """The screen to log the user into the system."""

    # Redirect the user if already logged in
    if current_user.is_authenticated:
        # Send admins and non-admins to different pages
        if current_user.admin:
            return redirect(url_for(default_admin_page))
        else:
            return redirect(url_for(default_user_page))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login.login'))
        login_user(user)
        current_app.logger.info(f"Logged in {user}")
        # If the user was redirected here, send the user back to the original page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # If no next page given, default to these pages
            if user.admin:
                next_page = url_for(default_admin_page)
            else:
                next_page = url_for(default_user_page)
        return redirect(next_page)
    nav_bar_title = "Login"
    return render_template('login/login.html', title='Sign in', form=form, nav_bar_title=nav_bar_title)


@bp.route('/logout')
@login_required
def logout():
    """ Logs the user out of the system. """
    current_app.logger.info(f"Logging out {current_user}")
    logout_user()
    return redirect(url_for('login.login'))


@bp.route('/end_all_sessions', methods=['POST'])
def end_all_sessions():
    """ Ends all user_sessions. This will stop all android sessions but does not log people out of flask_login"""
    user_ids = [user.id for user in User.query.all()]
    for user_id in user_ids:
        end_user_sessions(user_id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}





