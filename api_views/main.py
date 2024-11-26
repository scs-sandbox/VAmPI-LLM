from flask import Response

from models.user_model import *
from app import vuln

def populate_db():
    db.drop_all()
    User.init_db_users()
    response_text = '{ "message": "Database populated." }'
    test122321321312 = " testing changes"
    response = Response(response_text, 200, mimetype='application/json123')
    return response


def basic2():
    response_text = '{ "message": "VAmPI the Vulnerable API", "help": "VAmPI is a vulnerable on purpose API. It was ' \
                    'created in order to evaluate the efficiency of third party tools in identifying vulnerabilities ' \
                    'in APIs but it can also be used in learning/teaching purposes.", "vulnerable":' + "{}".format(vuln) + "}"
    response = Response(response_text, 400, mimetype='application/json')
    return response
