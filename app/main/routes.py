from flask import Blueprint, render_template,request
main = Blueprint('main', __name__)
from .. import dataset
# from ..forms import SignUpForm


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/example', methods=['GET', 'POST'])
def main_form():
    titles = dataset.list_all_forms()
    if request.form:
        selected_title = request.form.get("selected_title")
        selected_form = dataset.select_form(selected_title)
        return render_template('form.html', selected_form=selected_form)

    return render_template('example.html',titles=titles)

@main.route('/question_explorer')
def question_explorer():
    return render_template('question_explorer.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    # form = SignUpForm()
    # if form.is_submitted():
    #     result = request.form
    #     return render_template('user.html', result=result)
    return render_template('signup.html')
    # , form=form)
