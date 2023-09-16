from flask import Flask, flash, Blueprint, render_template, request, redirect, Response
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from Mystore import db
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
correct_password = 'b8b7ce3756a3abcd'

ig_f_2018_2016 = Blueprint('ig_f_2018_2016', __name__)


# Define the Text model
class Text5(db.Model):
    __bind_key__ = 'ig_f_2018_2016'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])


class AddTextForm5(FlaskForm):
    text_content5 = TextAreaField('Text Content', validators=[DataRequired()])


@ig_f_2018_2016.route('/ig_f_2018_2016_db', methods=['GET', 'POST'])
def index5():
    # Password is correct, render the protected page
    form = AddTextForm5()
    texts = Text5.query.all()
    return render_template('database/ig_f_2018_2016_db.html', texts=texts, form=form)

    # If it's a GET request or the form is invalid, show the password prompt


@ig_f_2018_2016.route('/add_text5', methods=['POST'])
def add_text5():
    form = AddTextForm5()
    if form.validate_on_submit():
        text_content5 = form.text_content5.data  # Use 'data' instead of 'content'
        if text_content5:
            new_text = Text5(content=text_content5)  # Use 'content' instead of 'data'
            db.session.add(new_text)
            db.session.commit()
            return redirect('/ig_f_2018_2016_db')
        else:
            flash('Text content cannot be empty.', 'warning')
    else:
        flash('Invalid form submission. Please check your input.', 'danger')

    # If form validation fails, return to the index page with error messages
    return redirect('/ig_f_2018_2016_db')


@ig_f_2018_2016.route('/download_text5')
def download_text5():
    text_to_download = Text5.query.first()
    if text_to_download:
        content = text_to_download.content.encode('utf-8')
        filename = 'downloaded_text5.txt'

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


@ig_f_2018_2016.route('/success/ig_f_2018_2016', methods=['GET'])
def download_after_payment():
    reference_id = request.args.get('reference')

    if is_valid_reference(reference_id):
        # Retrieve the text content from the database
        text_to_download = Text5.query.first()

        if text_to_download:
            content = text_to_download.content.encode('utf-8')
            filename = 'downloaded_text5.txt'

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
        return redirect('https://flutterwave.com/pay/ig_f_2018_2016')