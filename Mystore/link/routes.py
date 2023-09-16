from flask import Flask, flash, Blueprint, render_template, request, redirect, Response
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

link = Blueprint('link', __name__)


# Define the Text model
class Text17(db.Model):
    __bind_key__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm17(FlaskForm):
    text_content17 = TextAreaField('Text Content', validators=[DataRequired()])


@link.route('/link_db', methods=['GET', 'POST'])
def index17():
    # Password is correct, render the protected page
    form = AddTextForm17()
    texts = Text17.query.all()
    return render_template('database/link_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@link.route('/add_text17', methods=['POST'])
def add_text17():
    form = AddTextForm17()
    if form.validate_on_submit():
        text_content17 = form.text_content17.data  # Use 'data' instead of 'content'
        if text_content17:
            new_text = Text17(content=text_content17)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/link_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/link_db')


@link.route('/download_text17')
def download_text17():
    text_to_download = Text17.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text17.txt'

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


@link.route('/success/link', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text17.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text17.txt'

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
        return redirect('https://flutterwave.com/pay/linke')
