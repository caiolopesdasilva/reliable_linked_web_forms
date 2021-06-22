from SPARQLWrapper import SPARQLWrapper, JSON, POST
import shortuuid
from datetime import datetime

now = datetime.now()

sparql = SPARQLWrapper("http://localhost:8890/sparql/")  # RLWF Triple Store
sparql_wdt = SPARQLWrapper("https://query.wikidata.org/sparql",
                           agent="reliable_linked_web_forms_prototype; This is my master thesis at VU Amsterdam in "
                                 "the Netherlands see more on: https://github.com/caiolopesdasilva"
                                 "/reliable_linked_web_forms")  # Wikidata sparql link, this is very unstable.


# Without agent I was blacklisted from Wikidata. I'm not 100% sure what this does.


def list_all_forms():
    sparql.setQuery("""
        PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
        
        SELECT (str(?title) as ?Title) FROM <http://localhost:8890/RLWF> WHERE  {
          ?x RLWF:form_title ?title.
          ?x RLWF:form_counter ?counter.
        }
        order by ?counter
         """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    values = []
    for result in results["results"]["bindings"]:
        title = result["Title"]["value"]
        values.append(title)

    return values


def list_all_questions():
    sparql.setQuery("""
        PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
        
        SELECT DISTINCT (str(?x) as ?Question_Type) (str(?y) as ?wdt) 
        (str(?z)) as ?comment WHERE {
          ?entity a owl:Class.
          ?type rdfs:subClassOf* RLWF:Question.
          ?type rdfs:label ?x.
          ?type rdfs:comment ?z. 
        OPTIONAL {  ?type RLWF:containsWDT ?y.}
        }
        order by desc(?y)
         """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    values = []
    wdt = []
    comments = []
    for result in results["results"]["bindings"]:
        question = result["Question_Type"]["value"]
        rich_query = result["wdt"]["value"]
        com = result["comment"]["value"]
        values.append(question)
        wdt.append(rich_query)
        comments.append(com)

    return values, wdt, comments


def select_form(selected_title):
    sparql.setQuery("""
        PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
        
        SELECT (str(?title) as ?Title) (str(?counter) as ?Counter) (str(?desc) as ?Description)
        (str(?strdate) as ?Start_Date) (str(?enddate) as ?End_Date) FROM <http://localhost:8890/RLWF> WHERE  {
        
          ?x RLWF:form_title ?title.
          ?x RLWF:form_counter ?counter.
          ?x RLWF:form_description ?desc.
          ?x RLWF:form_startdate ?strdate. 
          ?x RLWF:form_enddate ?enddate.
        FILTER(regex(?title, '""" + selected_title + """')).
        }
        order by ?counter
             """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        title = (result["Title"]["value"])
        counter = result["Counter"]["value"]
        form_desc = result["Description"]["value"]
        str_date = result["Start_Date"]["value"]
        end_date = result["End_Date"]["value"]

    return title, counter, form_desc, str_date, end_date


def list_form_questions(selected_title):
    sparql.setQuery("""
        PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT (str(?counter) as ?qcounter) (str(?text) as ?text) (str(?q) as ?questiontype) (str(?wdt) as ?wdt)
        WHERE {
        
          ?x RLWF:hasQuestion ?entity.
          ?x RLWF:form_title ?form_title.
          ?entity a ?type.
          ?type rdfs:label ?q.
          ?type rdfs:subClassOf* RLWF:Question.
          ?entity RLWF:text ?text.
          ?entity RLWF:question_counter ?counter.
          OPTIONAL{?type RLWF:containsWDT ?wdt}.
        
        filter contains(str(?form_title),'""" + selected_title + """').
        }
        ORDER BY asc(?entity) 
                 """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    qcounter_array = []
    text_array = []
    qtypes_array = []
    wdt_array = []
    for result in results["results"]["bindings"]:
        qcounter = result["qcounter"]["value"]
        text = result["text"]["value"]
        question_type = result["questiontype"]["value"]
        wdt = result["wdt"]["value"]
        qcounter_array.append(qcounter)
        text_array.append(text)
        qtypes_array.append(question_type)
        wdt_array.append(wdt)

    return qcounter_array, text_array, qtypes_array, wdt_array


def respond_form(answers):
    sparql.setQuery("""

             """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        title = (result["Title"]["value"])
        counter = result["Counter"]["value"]

    return


def wdt_select_countries():
    sparql_wdt.setQuery("""
        SELECT ?country ?label_en
        WHERE
        {
          ?country wdt:P31 wd:Q6256.
          ?country rdfs:label ?label_en filter (lang(?label_en) = "en").
        }
        order by ?label_en
    """)
    sparql_wdt.setReturnFormat(JSON)
    results = sparql_wdt.query().convert()
    countries = []
    uris = []

    for result in results["results"]["bindings"]:
        country = (result["label_en"]["value"])
        uri = (result["country"]["value"])
        countries.append(country)
        uris.append(uri)

    return uri, countries


def wdt_nl_universities():
    sparql_wdt.setQuery("""
        SELECT DISTINCT ?university ?universityLabel ?cityLabel
        WHERE {
          ?university wdt:P31/wdt:P279* wd:Q38723 ;
                  wdt:P131 ?city .
          ?city wdt:P17 wd:Q55 .
          FILTER NOT EXISTS { ?statement pq:P582 ?university }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
          ?x rdfs:label ?universityLabel.     
           FILTER((LANG(?universityLabel)) = "en"). 
        }
        order by ?universityLabel
    """)
    sparql_wdt.setReturnFormat(JSON)
    results = sparql_wdt.query().convert()
    universities = []
    uni_uris = []

    for result in results["results"]["bindings"]:
        uni = (result["universityLabel"]["value"])
        uni_uri = result["university"]["value"]
        universities.append(uni)
        uni_uris.append(uni_uri)

    return uni_uris, universities


def wdt_communication_channels():
    sparql_wdt.setQuery("""
        SELECT ?social_media_uri ?label_en
        WHERE
        {
          ?social_media_uri wdt:P31 wd:Q3220391.
          ?social_media_uri rdfs:label ?label_en filter (lang(?label_en) = "en").
          filter not exists {?social_media_uri wdt:P576 ?x} #This line avoids defunct social network services
        }
    
        order by ?label_en
    """)
    sparql_wdt.setReturnFormat(JSON)
    results = sparql_wdt.query().convert()
    social_networks = []
    uris_social_media = []

    for result in results["results"]["bindings"]:
        social_network = (result["label_en"]["value"])
        uri_social_media = (result["social_media_uri"]["value"])
        social_networks.append(social_network)
        uris_social_media.append(uri_social_media)

    return uris_social_media, social_networks


def wdt_degrees():
    sparql_wdt.setQuery("""
        SELECT  ?degree_uri ?label_en
        WHERE
        {
          ?degree_uri wdt:P31/wdt:P279* wd:Q189533.
          ?degree_uri rdfs:label ?label_en filter (lang(?label_en) = "en").
          FILTER (contains(?label_en, "Bachelor")||
          contains(?label_en, "Master")||
          contains(?label_en,"PhD")).
        }
    
        order by ?label_en
    """)
    sparql_wdt.setReturnFormat(JSON)
    results = sparql_wdt.query().convert()
    degree_uris = []
    degree_names = []

    for result in results["results"]["bindings"]:
        degree_name = (result["label_en"]["value"])
        degree_uri = (result["degree_uri"]["value"])
        degree_names.append(degree_name)
        degree_uris.append(degree_uri)

    return degree_uris, degree_names


def check_agent(agent_name):
    sparql.setQuery("""
    PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
    ask 
    WHERE {
    ?person RLWF:agent_email ?email.
    filter contains(?email,'""" + agent_name + """')
    }
                     """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['boolean']


def get_agent_uid(email):
    sparql.setQuery("""
        PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
        select distinct (strafter(str(?person), "#") AS ?person)
        WHERE {
        ?person a owl:NamedIndividual.
        ?person RLWF:agent_email ?email.
        filter contains (?email,'""" + email + """')
        }

                         """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    uid = ""

    for result in results["results"]["bindings"]:
        uid = result["person"]["value"]

    return uid


def insert_new_agent(name, email):
    sparql.setMethod(POST)
    uuid = shortuuid.uuid()
    sparql.setQuery("""
    PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>

    INSERT DATA{
    GRAPH <http://localhost:8890/RLWF>
    {
    RLWF:""" + uuid + """ rdf:type owl:NamedIndividual ,
                      prov:Person ;
             RLWF:agent_email '""" + email + """'^^xsd:string ;
             RLWF:agent_name '""" + name + """'^^xsd:string .
    }
    }
    """)
    results = sparql.query()
    print(results.response.read())
    return uuid


def register_act_respond(uid):
    sparql.setMethod(POST)
    act_uid = shortuuid.uuid()
    sparql.setQuery("""
    PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>

    INSERT DATA{
    GRAPH <http://localhost:8890/RLWF>
    {
    RLWF:""" + act_uid + """ rdf:type owl:NamedIndividual ,
                            RLWF:RespondActivity ;
                      prov:hadRole RLWF:RespondentRole ;
                      prov:wasAssociatedWith RLWF:""" + uid + """ ;
                      prov:atTime "'""" + now.strftime("%d/%m/%YT%H:%M:%S") + """'"^^xsd:dateTime .
                      
                      
    }
    }
    """)
    results = sparql.query()
    print(results.response.read())
    return


def create_answer_cluster(uid):
    sparql.setMethod(POST)
    answer_cluster_id = shortuuid.uuid()
    sparql.setQuery("""
    PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>

    INSERT DATA{
    GRAPH <http://localhost:8890/RLWF>
    {
    RLWF:""" + answer_cluster_id + """ rdf:type owl:NamedIndividual ,
                     RLWF:AnswerCluster ;
            prov:wasAttributedTo RLWF:ID FROM AGENT HERE ;
            prov:wasGeneratedBy RLWF:ID FROM ACTIVITY HERE ;
            RLWF:hasIndividualAnswer RLWF:ID FROM UNIQUE ANSWER0 HERE ,
                                     RLWF:ID FROM UNIQUE ANSWER1 HERE ,
                                     RLWF:ID FROM UNIQUE ANSWER2 HERE ,
                                     RLWF:ID FROM UNIQUE ANSWER3 HERE ,
                                     RLWF:ID FROM UNIQUE ANSWER4 HERE ,
                                     RLWF:ID FROM UNIQUE ANSWER5 HERE ;
            RLWF:answerCluster_counter "COUNTER HERE"^^xsd:int .
    }
    }
    """)
    results = sparql.query()
    print(results.response.read())
    return


def reg_individual_answer():
    sparql.setMethod(POST)
    individual_answer_uid = shortuuid.uuid()
    sparql.setQuery("""
    PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>

    INSERT DATA{
    GRAPH <http://localhost:8890/RLWF>
    {
    RLWF:""" + individual_answer_uid + """ a owl:NamedIndividual ,
                            RLWF:IndividualAnswer ;
                    RLWF:hasAnswerTo RLWF:QUESTION_ID HERE, THIS IS GONNA BE COMPLICATED ;
                    RLWF:answer_counter "COUNTER FROM QUESTION HERE"^^xsd:int ;
        RLWF:individual_answer "THE VALUE OF THE ANSWER HERE^^xsd:string .
    }
    }
    """)
    results = sparql.query()
    print(results.response.read())
    return
