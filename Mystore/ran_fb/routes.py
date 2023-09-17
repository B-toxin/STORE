from flask import Flask, flash, Blueprint, Response, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

ran_fb = Blueprint('ran_fb', __name__)


# Define the Text model
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm(FlaskForm):
    text_content = TextAreaField('Text Content', validators=[DataRequired()])


@ran_fb.route('/ran_fb_db', methods=['GET', 'POST'])
def index():
    # Password is correct, render the protected page
    form = AddTextForm()
    texts = Text.query.all()
    return render_template('database/ran_fb_db.html', texts=texts, form=form)
    # If it's a GET request or the form is invalid, show the password prompt# Password is correct, render the protected page


@ran_fb.route('/add_text', methods=['POST'])
def add_text():
    form = AddTextForm()
    if form.validate_on_submit():
        text_content = form.text_content.data  # Use 'data' instead of 'content'
        if text_content:
            new_text = Text(content=text_content)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/ran_fb_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/ran_fb_db')


@ran_fb.route('/download_text')
def download_text():
    text_to_download = Text.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text.txt'

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


@ran_fb.route('/success/ran_fb', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text.txt'

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
        return redirect('https://flutterwave.com/pay/ran_fb')
