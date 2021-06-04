from flask import Blueprint, render_template,request
from ..forms import SignUpForm
main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/example', methods=['GET','POST'])
def main_form():
    form = formexample()
    if form.is_submitted():
        result = request.form
        return render_template('user.html',result=result)
    return render_template('example.html')


@main.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signup.html', form=form)
