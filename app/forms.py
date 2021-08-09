from app import dataset


def answer_processor(answers1, selected_title, form_instance, q_uids, q_types, countries, nl_universities, degrees,
                     communication_channels):
    countries_list = countries[1]
    countries_uris = countries[0]

    communication_channels_list = communication_channels[1]
    communication_channels_uris = communication_channels[0]

    nl_universities_list = nl_universities[1]
    nl_universities_uris = nl_universities[0]

    degrees_list = degrees[1]
    degrees_uris = degrees[0]

    #print(answers1)
    name = answers1[0]
    email = answers1[1]
    uni = answers1[2]
    channel = answers1[3]
    custom = answers1[4]
    country = answers1[5]
    individual_answers_name = []

    exists = dataset.check_agent(email)
    if exists:  # if the user is newly created the shortuuid is stored and returned from the function insert_new_agent
        # however if the user already exists we need to check the triple store for its agent_uid to create instances
        # of Activity, AnswerCluster, IndividualAnswer and so on.
        print("this user exists we will get his agent_uid")
        agent_uid = dataset.get_agent_uid(email)
    else:
        print("This is a new user, we are calling the insert_new_agent")
        agent_uid = dataset.insert_new_agent(name, email)

    prov_activity_id = dataset.register_act_respond(agent_uid)

    # after creating the activity, its best to generate each individual answer, one by one,
    # but we need to have some information from the form instance
    individual_answers_name = []  # this variable stores the names of each individual answer to be added
    # to the answer_cluster

    for x in range(len(answers1)):  # identify some unique types of questions to correctly call the right function
        if q_types[x] == "AcademicInformationQuestion":
            print("We have identified a AcademicInfoQuestion! We will send it to the right function")
            academic_info = [answers1[x]]
            newList = []
            for element in academic_info:
                newList.extend(element.split(','))  # this should give the degree and the uni in separate array indexes

            wdt_uri1 = degrees_uris[degrees_list.index(newList[0])]
            wdt_uri2 = nl_universities_uris[nl_universities_list.index(newList[1])]

            answer_uid = dataset.reg_wdt_individual_answer_2uri(answers1[x], q_uids[x], (str(x)), wdt_uri1, wdt_uri2)
            individual_answers_name.append(answer_uid)

        elif q_types[x] == "CommunicationChannelQuestion":
            print("We have identified a CommunicationChannelQuestion! We will send it to the right function")
            wdt_uri = communication_channels_uris[communication_channels_list.index(answers1[x])]
            answer_uid = dataset.reg_wdt_individual_answer_1uri(answers1[x], q_uids[x], (str(x)), wdt_uri)
            individual_answers_name.append(answer_uid)

        elif q_types[x] == "CountryQuestion":
            print("We have identified a CountryQuestion!! We will send it to the right function")
            wdt_uri = countries_uris[countries_list.index(answers1[x])]
            answer_uid = dataset.reg_wdt_individual_answer_1uri(answers1[x], q_uids[x], (str(x)), wdt_uri)
            individual_answers_name.append(answer_uid)

        else:
            print("We have identified a non-wdt question! We will send it to the right function")
            form_counter = dataset.get_cluster_counter(selected_title)
            answer_uid = dataset.reg_individual_answer(answers1[x], q_uids[x], (str(x)))
            individual_answers_name.append(answer_uid)

    # before creating the answer cluster its good to get the cluster_counter value.

    cluster_counter = dataset.get_cluster_counter(selected_title)
    cluster_counter = (int(cluster_counter)) + 1  # this convertion feels a bit rough for me, but it works.
    answer_cluster_uid = dataset.create_answer_cluster(individual_answers_name, prov_activity_id, agent_uid,
                                                       cluster_counter, form_instance)
    print("This Answer cluster was created" + answer_cluster_uid)