from SPARQLWrapper import SPARQLWrapper, JSON

endpoint="http://localhost:8890/sparql/"

def askClassProperty(uri):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        " PREFIX owl: <http://www.w3.org/2002/07/owl#> "
        " ASK WHERE {<" + uri + "> rdf:type owl:Class}")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print results
    for result in results:
        try:
            string = str(results[result])
            if "False" in string:
                return False

            if "True" in string:
                return True
        except:
            pass
    return False


def list_all_forms():
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery("""
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX RLWF: <https://raw.githubusercontent.com/caiolopesdasilva/reliable_linked_web_forms/main/onto/RLWF.owl#>
        PREFIX terms: <http://purl.org/dc/terms/>
        
        SELECT DISTINCT (str(?title) as ?title) (str(?order) as ?QuestionOrder) (str(?name) as ?participant)
        (str(?questiontxt) as ?question)  (str(?answer) as ?answer) WHERE {
          ?form terms:title ?title.
          ?form RLWF:hasQuestion ?question.
          ?query RLWF:text ?questiontxt.
          ?query RLWF:questionOrder ?order.
          ?answerinstance RLWF:answerClusterOrder ?instance.
          ?person RLWF:agent_name ?name.
          ?answerinstance prov:wasAttributedTo ?person.
          ?answerinstance RLWF:hasIndividualAnswer ?x.
          ?x RLWF:hasAnswerTo ?query.
          ?x RLWF:individual_answer ?answer
        }
        order by ?instance ?order 
         """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print results
    for result in results:
        try:
            string = str(results[result])
            if "False" in string:
                return False

            if "True" in string:
                return True
        except:
            pass
    return listallsforms()
