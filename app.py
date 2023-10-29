from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from person import Person
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_api_flask'
app.config['MYSQL_PASSWORD'] ='password'
app.config['MYSQL_DB'] = 'db_api_flask'

app.config['SECRET_KEY'] = 'app_123'

mysql = MySQL(app)


@app.route('/')
def index():
    return jsonify({"message": "API desarrollada con Flask"})


@app.route('/login', methods = ['POST'])
def login():
    auth = request.authorization
    print(auth)

    """ Control: existen valores para la autenticacion? """
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "No autorizado"}), 401       
            
    """ Control: existe y coincide el usuario en la BD? """
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (auth.username, auth.password))
    row = cur.fetchone()

    if not row:
       return jsonify({"message": "No autorizado"}), 401  
    
    """ El usuario existe en la BD y coincide su contraseña """
    token = jwt.encode({'id': row[0],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'])

    return jsonify({"token": token, "username": auth.username })

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print(kwargs)
        token = None


        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({"message": "Falta el token"}), 401
        
        try:
            data = jwt.decode(token , app.config['SECRET_KEY'], algorithms = ['HS256'])
            exp = data['exp']
            id = data['id']
        except Exception as e:
            print(e)
            return jsonify({"message": str(e)}), 401

        return func(*args, **kwargs)
    return decorated

@app.route('/test/<int:id>')
@token_required
def test(id):
    return jsonify({"message": "funcion test"})



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

    cur = mysql.connection.cursor()
    """ Control si existe el email indicado """
    cur.execute('SELECT * FROM person WHERE email = %s', (email,))
    row = cur.fetchone()

    if row:
        return jsonify({"message": "email ya registrado"})

    """ acceso a BD -> INSERT INTO """    
    cur.execute('INSERT INTO person (name, surname, dni, email) VALUES (%s, %s, %s, %s)', (name, surname, dni, email))
    mysql.connection.commit()

    """ obtener el id del registro creado """
    cur.execute('SELECT LAST_INSERT_ID()')
    row = cur.fetchone()
    print(row[0])
    id = row[0]
    return jsonify({"name": name, "surname": surname, "dni": dni, "email": email, "id": id})

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
    cur = mysql.connection.cursor()
    cur.execute('UPDATE person SET name = %s, surname = %s, dni = %s, email = %s WHERE id = %s', (name, surname, dni, email, id))
    mysql.connection.commit()
    return jsonify({"id": id, "name": name, "surname": surname, "dni": dni, "email": email})

@app.route('/persons/<int:id>', methods = ['DELETE'])
def remove_person(id):
    """ DELETE FROM WHERE... """
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM person WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return jsonify({"message": "deleted", "id": id})



















if __name__ == '__main__':
    app.run(debug=True, port=4500)