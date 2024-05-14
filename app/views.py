from flask import render_template, redirect, url_for
from app import app
from extensions import login_user, login_required, logout_user, current_user
from app.forms import UserForm, LoginForm, BookForm
from .services import BookService

@app.route('/', methods=['GET','POST'])
def index ():
    return render_template('home/index.html')

# create endpoint
@app.route('/cadastrar/', methods=['GET', 'POST'])
def cadastrar ():
    
    form = UserForm()
    
    if form.validate_on_submit():
        
        user = form.save()
        login_user(user, remember=True)

        return redirect( url_for('home') )
    
    return render_template('_partials/form-cadastrar-usuario.html', form=form)

# login endpoint
@app.route('/login/', methods=['GET', 'POST'])
def login ():
    
    form = LoginForm()

    if form.validate_on_submit():
        
        user = form.login()
        login_user(user, remember=True)

        return redirect(url_for('home'))

    return render_template('_partials/form-login.html', form=form)

# user home endpoint
@app.route('/home/', methods=['GET','POST'])
@login_required
def home ():
    book_service = BookService()
    books = book_service.get_books(current_user.id)
    return render_template('users/index.html', user=current_user, books=books)

# logout endpoint
@app.route('/sair/')
@login_required
def logout ():
    logout_user()
    return redirect(url_for('index'))

@app.route('/books/novo/', methods=['GET','POST'])
@login_required
def add_books ():
    
    form = BookForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('home'))
    
    return render_template('_partials/form-cadastrar-livro.html',form=form)
