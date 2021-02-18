from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):

    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):

    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}".format(self.text)


def insert_data():
    john = User(id=1, name='john')
    ethan = User(id=2, name='ethan')
    DB.session.add(john)
    DB.session.add(ethan)
    DB.session.commit()

