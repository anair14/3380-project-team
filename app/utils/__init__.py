from functools import wraps
from typing import Callable

from flask import redirect, url_for, flash
from flask_login import current_user


def complete_profile_required(view_function: Callable) -> Callable:
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and not current_user.profile_completed:
            flash('Please complete your profile before continuing.', 'warning')
            return redirect(url_for('edit_profile'))
        return view_function(*args, **kwargs)
    return decorated_function
