from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from src.data_fetcher import fetch_stock_data
import plotly.express as px
import plotly.io as pio
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'MaxNguyen': {'password': 'password123'}, 'OtherUser': {'password': 'password2345'}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@app.route('/stock_data')
@login_required
def stock_data():
    return render_template('stock_data.html')

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.id)

if __name__ == '__main__':
    app.run(debug=True)

from werkzeug.security import generate_password_hash, check_password_hash

users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.id)

@app.route('/stock_data', methods=['POST'])
@login_required
def stock_data():
    ticker = request.form['ticker']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    # Fetch stock data
    df = fetch_stock_data(ticker, start_date, end_date)
    # Create plot
    fig = px.line(df, x='Date', y='Close', title=f'{ticker} Stock Prices')
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('stock_data.html', graph_html=graph_html)

@app.route('/get_stock_data')
def get_stock_data():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    df = fetch_stock_data(ticker, start_date, end_date)
    return df.to_json()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    stock_data = db.relationship('StockData', backref='user', lazy=True)

class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

db.create_all()

@app.route('/save_stock_data', methods=['POST'])
@login_required
def save_stock_data():
    ticker = request.form['ticker']
    data = request.form['data']
    stock_data = StockData(ticker=ticker, data=data, user_id=current_user.id)
    db.session.add(stock_data)
    db.session.commit()
    flash('Stock data saved successfully!')
    return redirect(url_for('stock_data'))

@app.route('/view_saved_data')
@login_required
def view_saved_data():
    user_stock_data = StockData.query.filter_by(user_id=current_user.id).all()
    return render_template('view_saved_data.html', stock_data=user_stock_data)