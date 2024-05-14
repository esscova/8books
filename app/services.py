from .models import Books, Users

class UserService:
    def get_user(self, user_id):
        return Users.query.get(user_id)

class BookService:
    def get_books(self, user_id):
        return Books.query.filter_by(user_id=user_id).all()