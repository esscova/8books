from extensions import FlaskForm, bcrypt, db
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import Users, Books


class UserForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmacao_senha = PasswordField(
        "Confirmar a Senha", validators=[DataRequired(), EqualTo("senha")]
    )
    btnSubmit = SubmitField("Cadastrar")

    def validar_email(self, email):
        if Users.query.filter(email=email.data).first():
            return ValidationError("Este E-mail já está cadastrado!")

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode("utf-8"))
        user = Users(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha,
        )
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    btnSubmit = SubmitField("Login")

    def login(self):
        user = Users.query.filter_by(email=self.email.data).first()

        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode("utf-8")):
                return user
        else:
            raise Exception("Usuário ou Senha incorretos")

class BookForm(FlaskForm):
    autor = StringField('Autor', validators=[DataRequired()])
    titulo = StringField('Título', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    rate = SelectField('Classificação', validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')

    def save (self):
        book = Books(
            autor = self.autor.data,
            titulo = self.titulo.data,
            descricao=self.descricao.data,
            rate=self.rate.data
        )
        db.session.add(book)
        db.session.commit()

        return book