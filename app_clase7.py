from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from person import Person

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_api_flask'
app.config['MYSQL_PASSWORD'] ='password'
app.config['MYSQL_DB'] = 'db_api_flask'

mysql = MySQL(app)


@app.route('/')
def index():
    return jsonify({"message": "API desarrollada con Flask"})

@app.route('/persons', methods = ['GET'])
def get_all_persons():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM person')
    data = cur.fetchall()
    print(cur.rowcount)
    print(data)
    personList = []
    for row in data:
        objPerson = Person(row)
        personList.append(objPerson.to_json())
    return jsonify( personList )

""" @app.post('/persons') """
@app.route('/persons', methods = ['POST'])
def create_person():
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    dni = request.get_json()["dni"]
    email = request.get_json()["email"]

    """ acceso a BD -> INSERT INTO """
    return jsonify({"name": name, "surname": surname, "dni": dni, "email": email})

@app.route('/persons/<int:id>', methods = ['GET'])
def get_person_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM person WHERE id = {0}'.format(id))
    data = cur.fetchall()
    print(cur.rowcount)
    print(data)
    if cur.rowcount > 0:
        objPerson = Person(data[0])
        return jsonify( objPerson.to_json() )
    return jsonify( {"message": "id not found"} )

@app.route('/persons/<int:id>', methods = ['PUT'])
def update_person(id):
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    dni = request.get_json()["dni"]
    email = request.get_json()["email"]
    """ UPDATE SET ... WHERE ... """
    return jsonify({"id": id, "name": name, "surname": surname, "dni": dni, "email": email})

@app.route('/persons/<int:id>', methods = ['DELETE'])
def remove_person(id):
    """ DELETE FROM WHERE... """
    return jsonify({"message": "deleted", "id": id})



















if __name__ == '__main__':
    app.run(debug=True, port=4500)