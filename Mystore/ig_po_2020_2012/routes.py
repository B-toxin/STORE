from flask import Flask, flash, Blueprint, render_template, request, redirect, Response
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

ig_po_2020_2012 = Blueprint('ig_po_2020_2012', __name__)


# Define the Text model
class Text6(db.Model):
    __bind_key__ = 'ig_po_2020_2012'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm6(FlaskForm):
    text_content6 = TextAreaField('Text Content', validators=[DataRequired()])


@ig_po_2020_2012.route('/ig_po_2020_2012_db', methods=['GET', 'POST'])
def index6():
    # Password is correct, render the protected page
    form = AddTextForm6()
    texts = Text6.query.all()
    return render_template('database/ig_po_2020_2012_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@ig_po_2020_2012.route('/add_text6', methods=['POST'])
def add_text6():
    form = AddTextForm6()
    if form.validate_on_submit():
        text_content6 = form.text_content6.data  # Use 'data' instead of 'content'
        if text_content6:
            new_text = Text6(content=text_content6)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/ig_po_2020_2012_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/ig_po_2020_2012_db')


@ig_po_2020_2012.route('/download_text6')
def download_text6():
    text_to_download = Text6.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text6.txt'

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


@ig_po_2020_2012.route('/success/ig_po_2020_2012', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text6.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text6.txt'

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
        return redirect('https://flutterwave.com/pay/ig_po_2020_2012')
