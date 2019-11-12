"""Demo file from SQLAlchemy-1."""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = "SECRET!"


def connect_to_db(app, db_name):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)


class Cat(db.Model):
    """Feline catus."""

    __tablename__ = "cats"

    cat_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True,
                       )
    name = db.Column(db.String(50), nullable=False, unique=True,)
    color = db.Column(db.String(10), nullable=True,)
    hunger = db.Column(db.Integer, nullable=False, default=20,)

    def greet(self):
        """Greet using name."""

        return f"I am {self.name}"

    def feed(self, units=10):
        """Nom nom nom."""

        self.hunger -= units
        self.hunger = max(self.hunger, 0)

    @classmethod
    def get_by_color(cls, color):
        """Get all cats matching that color."""

        return cls.query.filter_by(color=color).all()

    def __repr__(self):
        """Show info about cat."""

        return f"<Cat id={self.cat_id} name={self.name}"


if __name__ == "__main__":
    connect_to_db(app, "cats")

    # Create all tables
    db.create_all()

    # If table isn't empty, empty it
    Cat.query.delete()

    # Add cats
    auden = Cat(name="Auden", color="grey")
    felix = Cat(name="Felix", color="grey", hunger=10)
    ezra = Cat(name="Ezra", color="orange")

    # Add new objects to session, so they'll persist
    db.session.add(auden)
    db.session.add(felix)
    db.session.add(ezra)

    # Commit--otherwise, this never gets saved!
    db.session.commit()
