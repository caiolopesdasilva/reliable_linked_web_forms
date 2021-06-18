from flask import Blueprint, render_template, request, redirect, url_for, session
from .. import dataset

main = Blueprint('main', __name__)
main.secret_key = "hello"


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
        session["form_title"] = selected_title
        return redirect(url_for("main.list_form"))
    else:
        titles = dataset.list_all_forms()
        return render_template('example.html', titles=titles)


@main.route("/list_form", methods=['GET', 'POST'])
def list_form():
    countries = []  # we need a set of empty lists so that the return template can correctly load if question types are
    # not in the form.
    degrees = ["Bachelor's Degree", "Master's Degree", "Doctoral Degree"]
    nl_universities = []
    communication_channels = ["Facebook"]
    if "form_title" in session:
        selected_title = session["form_title"]
        selected_form = dataset.select_form(selected_title)
        list_questions = dataset.list_form_questions(selected_title)
        counters = list_questions[0]
        questions = list_questions[1]
        q_types = list_questions[2]
        wdt = list_questions[3]

        for i in range(len(q_types)):  # find the country question
            if wdt[i] == "1":
                if q_types[i] == "CountryQuestion":
                    countries = dataset.wdt_select_countries()
                if q_types[i] == "AcademicInformationQuestion":
                    nl_universities = dataset.wdt_nl_universities()

                # if q_types[i] == "CommunicationChannelQuestion":
                #     communication_channels = dataset.wdt_communication_channels()

        if request.method == "POST":
            for i in range(len(counters)):
                answers1 = []
                answers = request.form["answer" + (str(i))]
                answers1.append(answers)
                dataset.respond_form(answers1)
        return render_template('form.html', selected_form=selected_form, counters=counters, questions=questions,
                               q_types=q_types, countries=countries, degrees=degrees, nl_universities=nl_universities,
                               communication_channels=communication_channels)
    else:
        return redirect(url_for("main.index"))


@main.route('/question_explorer', methods=['GET', 'POST'])
def question_explorer():
    questions = dataset.list_all_questions()

    list_of_questions = questions[0]
    wdt = questions[1]
    question_comments = questions[2]
    comments = []
    wikidata_queryable = []
    countries = []
    if request.method == "POST":
        question_select = request.form["question_select"]
        for x in range(len(questions)):
            if list_of_questions[x] == "CountryQuestion":
                countries = dataset.wdt_select_countries()
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


@main.route('/teste', methods=['GET', 'POST'])
def teste():
    return render_template('teste.html')
