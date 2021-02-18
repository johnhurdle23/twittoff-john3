from flask import Flask, render_template, request
from models import DB, User, insert_data
from twitter import add_or_update_user
from predict import predict_user

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/', methods=['GET'])
    def landing():
        DB.drop_all()
        DB.create_all()
        example_users = ['elonmusk', 'katyperry', 'rihanna', 'barackobama']
        for user in example_users:
            add_or_update_user(user)
        return render_template("hello.html", title="Lambda3.3.1", users=User.query.all())

    @app.route('/compare', methods=['POST'])
    def compare():
        user1 = request.form['selected_user_1']
        user2 = request.form['selected_user_2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = "Cannot comoare the same user to itself"

        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = str(prediction) + " is more likely to have said " + str(tweet_text)

        return render_template('prediction.html', title="Predict Tweet Author", message=message)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()