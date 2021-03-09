from flask import Blueprint, render_template,request
from ..forms import SignUpForm
main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/examples')
def examples():
    return render_template('examples.html')


@main.route('/blog/<int:blog_id>')
def blogpost(blog_id):
    return 'This is the blogpost number' + str(blog_id)

@main.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signup.html', form=form)
