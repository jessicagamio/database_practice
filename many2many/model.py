from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_to_db(app, db_name):
    """connect ot db"""
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    # app.config['SQLALCHEMY_ECHO']=True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app= app
    db.init_app(app)


class Book(db.Model):
    """Book"""
    __tablename__='books'

    book_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))

    comments=db.relationship('Comment')
    bookgenre= db.relationship('BookGenre')

    def __repr__(self):
        return f'<Book title={self.title}>'

class Genre(db.Model):
    """Genre"""
    __tablename__= 'genre'
    genre_id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    genre = db.Column(db.String(50), nullable=False)

    book= db.relationship('Book', secondary='bookgenre', backref='genre')
    
    def __repr__(self):
        return f'<Genre genre={self.genre}>'

class Category(db.Model):

    __tablename__='category'
    cat_id=db.Column(db.Integer, primary_key=True,autoincrement=True)

    def __repr__(self):
        return f'<Category cat_id={self.cat_id}>'

class BookGenre(db.Model):
    """Book Genre"""
    __tablename__='bookgenre'

    bookgenre_id=db.Column(db.Integer, primary_key=True, autoincrement=True)

    book_id=db.Column(db.Integer,db.ForeignKey('books.book_id'))
    genre_id=db.Column(db.Integer, db.ForeignKey('genre.genre_id'))

    book=db.relationship('Book')
    genre=db.relationship('Genre')


class User(db.Model):
    """User"""
    __tablename__='users'

    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(50))

    book=db.relationship('Book', secondary='comments',backref='users')
    comments=db.relationship('Comment')

    def __repr__(self):
        return f'<User email={self.email} user_id={self.user_id}>'


class Comment(db.Model):
    """comments"""

    __tablename__='comments'

    comment_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id=db.Column(db.Integer, db.ForeignKey('books.book_id'))
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    body=db.Column(db.Text, nullable=False)

    book= db.relationship('Book')
    user=db.relationship('User')

    def __repr__(self):
        return f'<Comment book={self.book} user={self.user} body={self.body}>'



jim=User(email='jim@gmail.com')
Harry=User(email='potter@gmail.com')
Abby=User(email='Abby@gmail.com')

Fellowship=Book(title='Lord of the Rings')
Night=Book(title='Night')
Leonardo=Book(title='Leonardo da Vinci')

Fellowshipgenre=Genre(genre='Fantasy')
FellowshipgenreConnect=BookGenre(book=Fellowship, genre=Fellowshipgenre)

Nightgenre=Genre(genre='Fictior')
NightgenreConnect=BookGenre(book=Night, genre=Nightgenre)

Leonardogenre=Genre(genre='Biography')
LeonardogenreConnect=BookGenre(book=Leonardo, genre=Leonardogenre)

jimcomm=Comment(body='I am off two a new adventure!!', book=Fellowship, user=jim)
Harrycomm=Comment(body='I am off two a new adventure!!', book=Night, user=Harry)
Harrycomm1=Comment(body='I am off two a new adventure!!', book=Fellowship, user=Harry)
Abbycomm=Comment(body='I am off two a new adventure!!', book=Leonardo, user=Abby)

if __name__=="__main__":
    from server import app
    connect_to_db(app, 'bookstore')
    db.create_all()



    db.session.add(jim)
    db.session.commit()
    db.session.add(Fellowship)
    db.session.commit()
    db.session.add(jimcomm)
    db.session.commit()
    db.session.add(Harry)
    db.session.commit()
    db.session.add(Abby)
    db.session.commit()
    db.session.add(Night)
    db.session.commit()
    db.session.add(Leonardo)
    db.session.commit()
    db.session.add(Harrycomm)
    db.session.add(Harrycomm1)
    db.session.add(Abbycomm)
    db.session.commit()
    db.session.add(Fellowshipgenre)
    db.session.add(Nightgenre)
    db.session.add(Leonardogenre)
    db.session.commit()
    db.session.add(FellowshipgenreConnect)
    db.session.add(NightgenreConnect)
    db.session.add(LeonardogenreConnect)
    db.session.commit()


