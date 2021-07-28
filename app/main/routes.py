from flask import Blueprint, render_template, request, redirect, url_for
from .. import dataset, forms

main = Blueprint('main', __name__)

titles = dataset.list_all_forms()
countries = dataset.wdt_select_countries()
nl_universities = dataset.wdt_nl_universities()
all_questions = dataset.list_all_questions()  # this is used in the /question_explorer
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
    wdt = list_questions[3]  # wdt enabled should appear in the metadada from the question
    q_uids = list_questions[4]
    form_instance = list_questions[5]  # this will only contain 1 value

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
        forms.answer_processor(answers1, selected_title, form_instance, q_uids, q_types, countries, nl_universities,
                               degrees, communication_channels)

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

    if request.method == "POST":
        question_select = request.form["question_select"]
        c_question = dataset.get_question_information(question_select)
        y = dataset.wdt_custom_question(c_question[1], c_question[2])
        print(y)
        question_index = list_of_questions.index(question_select)
        comment = question_comments[question_index]
        wikidata_queryable = wdt[question_index]

        # isIndex is the variable we will use to determine
        # whether or not to render the metadata from the questions,
        # I think this is very rough but as in cases before, it works.
        return render_template("question_explorer.html", list_of_questions=list_of_questions,
                               comment=comment, wikidata_queryable=wikidata_queryable, countries=countries[1],
                               question_select=question_select, degrees=degrees[1], nl_universities=nl_universities[1],
                               communication_channels=communication_channels[1], isIndex=True, c_question=c_question[0],
                               c_q_values=y[1])

    else:
        return render_template('question_explorer.html', list_of_questions=list_of_questions, isIndex=False)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@main.route('/question_creator', methods=['GET', 'POST'])
def question_creator():
    if request.method == "POST":
        question_name = request.form["input_q_name"]
        entity_id = request.form["entity_id"]
        query_filter = request.form["filter"]
        comments = request.form["comments"]

        exists = dataset.custom_question_analyser(entity_id)

        # if exists:
        # print("this entity_id is already registered, we cannot create it")
        # return render_template('question_creator.html')

        # else:
        print("This is a entity_id, we will create the new question type.")
        dataset.register_custom_question(question_name, entity_id, query_filter, comments);
        global all_questions
        all_questions = []
        all_questions = dataset.list_all_questions()
        custom_question = dataset.wdt_custom_question(entity_id, query_filter)
        print(custom_question)

        return render_template('question_creator.html')

    else:
        return render_template('question_creator.html')
