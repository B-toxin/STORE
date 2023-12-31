from flask import Flask, flash, Blueprint, Response, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

link_200 = Blueprint('link_200', __name__)


# Define the Text model
class Text15(db.Model):
    __bind_key__ = 'link_200'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm15(FlaskForm):
    text_content15 = TextAreaField('Text Content', validators=[DataRequired()])


@link_200.route('/link_200_db', methods=['GET', 'POST'])
def index15():
    # Password is correct, render the protected page
    form = AddTextForm15()
    texts = Text15.query.all()
    return render_template('database/link_200_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@link_200.route('/add_text15', methods=['POST'])
def add_text15():
    form = AddTextForm15()
    if form.validate_on_submit():
        text_content15 = form.text_content15.data  # Use 'data' instead of 'content'
        if text_content15:
            new_text = Text15(content=text_content15)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/link_200_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/link_200_db')


@link_200.route('/download_text15')
def download_text15():
    text_to_download = Text15.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text15.txt'

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


@link_200.route('/success/link_200', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text15.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text15.txt'

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
        return redirect('https://flutterwave.com/pay/link_200')
