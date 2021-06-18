from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = "http://localhost:8890/sparql/"
sparql = SPARQLWrapper(endpoint)


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
    sparql1 = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql1.setQuery("""
    SELECT ?country ?label_en
    WHERE
    {
      ?country wdt:P31 wd:Q6256.
      ?country rdfs:label ?label_en filter (lang(?label_en) = "en").
    }

    order by ?label_en
    """)
    sparql1.setReturnFormat(JSON)
    results = sparql1.query().convert()
    countries = []

    for result in results["results"]["bindings"]:
        country = (result["label_en"]["value"])
        countries.append(country)

    return countries


def wdt_nl_universities():
    sparql1 = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql1.setQuery("""
    SELECT DISTINCT ?universityLabel ?cityLabel
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
    sparql1.setReturnFormat(JSON)
    results = sparql1.query().convert()
    universities = []

    for result in results["results"]["bindings"]:
        uni = (result["universityLabel"]["value"])
        universities.append(uni)

    return universities


def wdt_communication_channels():
    sparql1 = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql1.setQuery("""
    SELECT ?country ?label_en
    WHERE
    {
      ?country wdt:P31 wd:Q6256.
      ?country rdfs:label ?label_en filter (lang(?label_en) = "en").
    }

    order by ?label_en
    """)
    sparql1.setReturnFormat(JSON)
    results = sparql1.query().convert()
    countries = []

    for result in results["results"]["bindings"]:
        country = (result["label_en"]["value"])
        countries.append(country)

    return countries
