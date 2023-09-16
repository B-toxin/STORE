from flask import Flask, flash, Blueprint, render_template, request, redirect, Response
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

link_100 = Blueprint('link_100', __name__)


# Define the Text model
class Text14(db.Model):
    __bind_key__ = 'link_100'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm14(FlaskForm):
    text_content14 = TextAreaField('Text Content', validators=[DataRequired()])


@link_100.route('/link_100_db', methods=['GET', 'POST'])
def index14():
    # Password is correct, render the protected page
    form = AddTextForm14()
    texts = Text14.query.all()
    return render_template('database/link_100_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@link_100.route('/add_text14', methods=['POST'])
def add_text14():
    form = AddTextForm14()
    if form.validate_on_submit():
        text_content14 = form.text_content14.data  # Use 'data' instead of 'content'
        if text_content14:
            new_text = Text14(content=text_content14)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/link_100_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/link_100_db')


@link_100.route('/download_text14')
def download_text14():
    text_to_download = Text14.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text14.txt'

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


@link_100.route('/success/link_100', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text14.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text14.txt'

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
        return redirect('https://flutterwave.com/pay/link_100')
