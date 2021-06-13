from SPARQLWrapper import SPARQLWrapper, JSON

endpoint="http://localhost:8890/sparql/"
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

    values=[]
    for result in results["results"]["bindings"]:
        title=result["Title"]["value"]
        values.append(title)

    return values


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
FILTER(regex(?title, '"""+selected_title+"""')).
}
order by ?counter
             """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    form_desc = []
    for result in results["results"]["bindings"]:
        title = (result["Title"]["value"])
        counter = result["Counter"]["value"]
        form_desc = result["Description"]["value"]
        str_date = result["Start_Date"]["value"]
        end_date =  result["End_Date"]["value"]

    return title, counter, form_desc, str_date, end_date


def list_form_questions(selected_title):
    sparql.setQuery("""
PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (str(?counter) as ?Counter) (str(?text) as ?text) (str(?type) as ?Type) (str(?q) as ?Question_Type)
WHERE {
  ?entity a ?type.
  ?type rdfs:label ?q.
  ?type rdfs:subClassOf* RLWF:Question.
  ?entity RLWF:text ?text.
  ?entity RLWF:question_counter ?counter.

 filter contains(str(?entity),'"""+selected_title+"""').
}
ORDER BY asc(?entity)
                 """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    form_desc = []
    for result in results["results"]["bindings"]:
        title = (result["Title"]["value"])
        counter = result["Counter"]["value"]
        form_desc = result["Description"]["value"]
        str_date = result["Start_Date"]["value"]
        end_date = result["End_Date"]["value"]

    return title, counter, form_desc, str_date, end_date


    return

# def askClassProperty(uri):
#     sparql = SPARQLWrapper(endpoint)
#     sparql.setQuery(
#         "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
#         " PREFIX owl: <http://www.w3.org/2002/07/owl#> "
#         " ASK WHERE {<" + uri + "> rdf:type owl:Class}")
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     # print results
#     for result in results:
#         try:
#             string = str(results[result])
#             if "False" in string:
#                 return False
#
#             if "True" in string:
#                 return True
#         except:
#             pass
#     return False

