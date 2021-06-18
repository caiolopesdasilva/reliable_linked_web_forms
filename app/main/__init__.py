from flask import Blueprint
from .. import dataset

main = Blueprint('main', __name__)
main.secret_key = "hello"
