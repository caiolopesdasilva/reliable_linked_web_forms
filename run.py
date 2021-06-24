from app import create_app

print("...The initial load will store all wikidata queries, this can take up to 30 seconds")
if __name__ == '__main__':
    create_app().run(use_reloader=False)

