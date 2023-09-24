from flask import Flask, jsonify, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index'

@app.route('/ping')
def ping():
    return jsonify({"message": "pong"})

@app.route('/usuarios/<string:nombre>') #json de un texto ---> /usuarios/juan
def usuario_by_name(nombre):
    return jsonify({"name" : nombre})

@app.route('/usuarios/<int:id>')       #json de un numero ---> /usuarios/3
def usuario_by_id(id):
    return jsonify({"id": id})

@app.route('/<path:nombre>')          #escape de cadena mensaje emergente
def no_hacer(nombre):
    return escape(nombre)


# GET todos los 'recursos'
@app.route('/recurso', methods = ['GET'])
def get_recursos():
    return jsonify({"data": "lista de todos los items de este recurso"})

# POST nuevo 'recurso'
@app.route('/recurso', methods = ['POST']) # espera resivir variables locales (request)
def post_recurso():
    print(request.get_json())
    body = request.get_json()
    name = body["name"]                    # espera la clave - valor ---> "name"
    modelo = body["modelo"]                # espera la clave - valor ---> "modelo"
    # insertar en la BD 
    return jsonify({"recurso": {
        "name": name,
        "modelo": modelo
    }})

# GET un 'recurso' a traves de su id
@app.route('/recurso/<int:id>', methods = ['GET'])  #json de un objeto segun un num de Id ---> /recurso/3
def get_recurso_by_id(id):
    # buscar en la BD un registro con ese id
    return jsonify({"recurso":{
        "name": "nombre correspondiente a ese id",
        "modelo": "modelo correspondiente a ese id"
    }})








if __name__ == '__main__':
    app.run(debug=True, port=5000)