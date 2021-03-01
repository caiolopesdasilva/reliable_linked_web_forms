from app import create_app

os.environ['FLASK_ENV'] = 'development'

if __name__ == '__main__':
    create_app().run(debug=True)
