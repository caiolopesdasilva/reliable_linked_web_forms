from flask import Blueprint, render_template

main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return 'The about page'

@main.route('/blog')
def blog():
    return 'This is the blog'

@main.route('/blog/<int:blog_id>')
def blogpost(blog_id):
    return 'This is the blogpost number' + str(blog_id)