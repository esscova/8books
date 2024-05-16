from flask import render_template, redirect, url_for, request, jsonify
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
@app.route('/home/', methods=['GET','POST','PUT','DELETE'])
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

@app.route('/book/edit/<int:book_id>/', methods=['GET','PUT'])
@login_required
def editar_livro (book_id):
    
    form=BookForm()
    book_service = BookService()
    book = book_service.get_book(book_id=book_id)

    if book.user_id != current_user.id:
        return "permissão negada"
    
    if request.method == 'GET':
        form.autor.data = book.autor
        form.titulo.data = book.titulo
        form.categoria.data = book.categoria
        form.descricao.data = book.descricao
        form.rate.data = book.rate
        return render_template('_partials/form-editar-livro.html', form=form, book=book)

    if request.method == 'PUT':
        if form.validate_on_submit():
            form.populate_obj(book)
            book_service.update_book(book)

            return render_template('/_partials/book_row.html', book=book)
            # return redirect(url_for('home'))
    return jsonify({'errors': form.errors}), 400
            
           
    
@app.route('/book/delete/<int:book_id>/', methods=['DELETE'])
@login_required
def excluir_livro(book_id):
    if request.method == 'DELETE':
        book_service = BookService()
        book = book_service.get_book(book_id)

        if not book:
            return 'livro não encontrado',404

        if book.user_id != current_user.id:
            return 'operação não permitida',403
        
        book_service.delete_book(book)
        return ""

@app.route('/get_book/<int:book_id>')
@login_required
def get_book(book_id):
    book_service = BookService()
    book=book_service.get_book(book_id=book_id)
    return render_template('_partials/book_row.html', book=book)

@app.route('/get-form/<int:book_id>')
@login_required
def get_form(book_id):
    form=BookService()
    
    book_service = BookService()
    book=book_service.get_book(book_id=book_id)

    form.autor.data = book.autor
    form.titulo.data = book.titulo
    form.categoria.data = book.categoria
    form.descricao.data = book.descricao
    form.rate.data = book.rate

    render_template('_partials/form-editar-livro.html', book=book, form=form)