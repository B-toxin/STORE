from flask import Flask, flash, Blueprint, Response, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

aged_reddit = Blueprint('aged_reddit', __name__)


# Define the Text model
class Text12(db.Model):
    __bind_key__ = 'aged_reddit'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm12(FlaskForm):
    text_content12 = TextAreaField('Text Content', validators=[DataRequired()])


@aged_reddit.route('/aged_reddit_db', methods=['GET', 'POST'])
def index12():
    # Password is correct, render the protected page
    form = AddTextForm12()
    texts = Text12.query.all()
    return render_template('database/aged_reddit_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@aged_reddit.route('/add_text12', methods=['POST'])
def add_text12():
    form = AddTextForm12()
    if form.validate_on_submit():
        text_content12 = form.text_content12.data  # Use 'data' instead of 'content'
        if text_content12:
            new_text = Text12(content=text_content12)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/aged_reddit_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/aged_reddit_db')


@aged_reddit.route('/download_text12')
def download_text12():
    text_to_download = Text12.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text12.txt'

        db.session.delete(text_to_download)
        db.session.commit()

        return Response(
            content,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Length': len(content)
            }
        )
    else:
        return "No more texts to download."


# Function to check if the reference ID is valid (e.g., in a database)
def is_valid_reference(reference_id):
    return reference_id is None


@aged_reddit.route('/success/aged_reddit', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text12.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text12.txt'

            db.session.delete(text_to_download)
            db.session.commit()

            return Response(
                content,
                mimetype='text/plain',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Length': len(content)
                }
            )
        else:
            return "No more texts to download."
    else:
        return redirect('https://flutterwave.com/pay/aged_reddit')
