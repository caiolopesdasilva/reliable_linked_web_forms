from app import dataset


def answer_processor(answers1):
    print(answers1)
    name = answers1[0]
    email = answers1[1]
    uni = answers1[2]
    channel = answers1[3]
    custom = answers1[4]
    country = answers1[5]

    exists = dataset.check_agent(email)
    if exists:  # if the user is newly created the shortuuid is stored and returned from the function insert_new_agent
        # however if the user already exists we need to check the triple store for its uid to create instances
        # of Activity, AnswerCluster, IndividualAnswer and so on.
        print("this user exists we will get his uid")
        uid = dataset.get_agent_uid(email)
        dataset.register_act_respond(uid)
            for x in range(len(answers1)):
            dataset.reg_individual_answer(uid) #after creating the activity, its best to generate each individual answer
        dataset.create_answer_cluster(uid)
    else:
        print("This is a new user, we are calling the insert_new_agent")
        uid = dataset.insert_new_agent(name, email)
        dataset.register_act_respond(uid)
        dataset.reg_individual_answer(uid)
        dataset.create_answer_cluster(uid)
