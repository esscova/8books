from .models import Books, Users
from extensions import db

class UserService:
    def get_user(self, user_id):
        return Users.query.get(user_id)

class BookService:
    def get_books(self, user_id):
        return Books.query.filter_by(user_id=user_id).all()
    
    def get_book(self, book_id):
        return Books.query.get_or_404(book_id)
    
    def update_book(self, book):
        db.session.commit()
    
    def delete_book(self, book):
        db.session.delete(book)
        db.session.commit()