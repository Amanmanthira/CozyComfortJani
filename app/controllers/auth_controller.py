from flask import Blueprint, render_template, request, redirect, session
from app.services.auth_service import login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)
        if user:
            session['user'] = user
            role = user['role']
            if role == 'manufacturer':
                return redirect('manufacturer/dashboard')
            elif role == 'distributor':
                return redirect('/distributor/dashboard')
            elif role == 'seller':
                return redirect('/seller/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

