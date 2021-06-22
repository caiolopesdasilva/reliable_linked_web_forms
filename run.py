from app import create_app

if __name__ == '__main__':
    print("...The initial load will store all wikidata queries, this can take up to 30 seconds")
    create_app().run(debug=True)

