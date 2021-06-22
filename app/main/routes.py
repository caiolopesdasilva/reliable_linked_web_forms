from flask import Blueprint, render_template, request, redirect, url_for
from .. import dataset
from .. import forms

main = Blueprint('main', __name__)
main.secret_key = "hello"

titles = dataset.list_all_forms()
countries = dataset.wdt_select_countries()
nl_universities = dataset.wdt_nl_universities()
all_questions = dataset.list_all_questions()
degrees = dataset.wdt_degrees()
communication_channels = dataset.wdt_communication_channels()


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/example', methods=['GET', 'POST'])
def main_form():
    if request.method == "POST":
        selected_title = request.form["selected_title"]
        return redirect(url_for("main.list_form", selected_title=selected_title))
    else:
        # titles = dataset.list_all_forms()
        return render_template('example.html', titles=titles)


@main.route("/list_form-<selected_title>", methods=['GET', 'POST'])
def list_form(selected_title):
    selected_form = dataset.select_form(selected_title)
    list_questions = dataset.list_form_questions(selected_title)
    counters = list_questions[0]
    questions = list_questions[1]
    q_types = list_questions[2]
    wdt = list_questions[3]
    countries_list = countries[1]
    social_media_list = communication_channels[1]
    degrees_list = degrees[1]
    unis_list = nl_universities[1]

    if request.method == "POST":
        answers1 = []
        for i in range(len(counters)):
            if q_types[i] == "AcademicInformationQuestion":
                answers = request.form["degree"] + "," + request.form["answer" + (str(i))]
                answers1.append(answers)
            else:
                answers = request.form["answer" + (str(i))]
                answers1.append(answers)
        forms.answer_processor(answers1)

    return render_template('form.html', selected_form=selected_form, counters=counters, questions=questions,
                           q_types=q_types, countries=countries_list, degrees=degrees_list,
                           nl_universities=unis_list,
                           communication_channels=social_media_list)


@main.route('/form_answer', methods=['GET', 'POST'])
def form_answer():
    return render_template('form_answered.html')


@main.route('/question_explorer', methods=['GET', 'POST'])
def question_explorer():
    list_of_questions = all_questions[0]
    wdt = all_questions[1]
    question_comments = all_questions[2]
    comments = []
    wikidata_queryable = []
    if request.method == "POST":
        question_select = request.form["question_select"]
        for x in range(len(all_questions)):
            comments = question_comments[x]
            wikidata_queryable = wdt[x]
            print(comments)

        # isIndex is the variable we will use to determine
        # whether or not to render the metadata from the questions,
        # I think this is very rough but as in cases before, it works.
        return render_template("question_explorer.html", list_of_questions=list_of_questions,
                               comments=comments, wikidata_queriable=wikidata_queryable, countries=countries,
                               question_select=question_select, isIndex=True)

    else:
        return render_template('question_explorer.html', list_of_questions=list_of_questions)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')
