# Importación de módulos necesarios
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
import datetime

#Creacion de APP Flask
app = Flask(__name__)
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/test'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

#Definimo el modelo de datos
class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100))
    modelo= db.Column(db.String(100))
    anio= db.Column(db.String(16))
    patente= db.Column(db.String(20))
    pais_origen= db.Column(db.String(30))
    
    def __init__(self,marca,modelo,anio,patente,pais_origen):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.patente = patente
        self.pais_origen = pais_origen

#Definimos el esquema
class AutoSchema(ma.Schema):
    class Meta:
        fields = ('id','marca','modelo','anio','patente','pais_origen')


#Crear esquemas para la db
auto_schema = AutoSchema() #trae un auto
autos_schema = AutoSchema(many=True) #Para traer más de un auto

#Creamos la tablas
with app.app_context():
    db.create_all()

#Endpoint Get
@app.route('/autos', methods=['GET'])
def get_all_autos():
    try:
        autos = Auto.query.all()
        if autos:
            return autos_schema.jsonify(autos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Endpoint Get by Id
@app.route('/autos/<id>', methods=['GET'])
def get_auto(id):
    try:
        auto = Auto.query.get(id)

        if auto:
            return auto_schema.jsonify(auto)
        else:
            return jsonify({'error': 'Auto no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo auto mediante una solicitud POST
@app.route('/autos', methods=['POST'])
def create_auto():
    try:
        json_data = request.get_json()
        marca = json_data['marca']
        modelo = json_data['modelo']
        anio = json_data['anio']
        patente = json_data['patente']
        pais_origen = json_data['pais_origen']

        # Cargar datos JSON en un objeto auto
        nuevo_auto = Auto(marca, modelo, anio, patente, pais_origen)

        # Realizar validaciones adicionales si es necesario

        db.session.add(nuevo_auto)
        db.session.commit()

        return auto_schema.jsonify(nuevo_auto), 201  # Devolver el auto creado con el código 201 (creado)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para actualizar un auto mediante una solicitud PUT
@app.route('/autos/<id>', methods=['PUT'])
def update_auto(id):
    try:
        auto = Auto.query.get(id)

        # Verificar si el auto existe en la base de datos
        if auto:
            json_data = request.get_json()
            auto.marca = json_data.get('marca', auto.marca)
            auto.modelo = json_data.get('modelo', auto.modelo)
            auto.anio = json_data.get('dni', auto.anio)
            auto.patente = json_data.get('patente', auto.patente)
            auto.pais_origen = json_data.get('pais_origen', auto.pais_origen)

            # Realizar validaciones según tus requerimientos

            db.session.commit()
            return auto_schema.jsonify(auto)
        else:
            return jsonify({'error': 'Auto no encontrado'}), 404  # Devolver código 404 si el auto no existe

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para eliminar un auto mediante una solicitud DELETE
@app.route('/autos/<id>', methods=['DELETE'])
def delete_auto(id):
    try:
        auto = Auto.query.get(id)

        # Verificar si el auto existe en la base de datos
        if auto:
            db.session.delete(auto)
            db.session.commit()
            return auto_schema.jsonify(auto)
        else:
            return jsonify({'error': 'Auto no encontrado'}), 404  # Devolver código 404 si el auto no existe

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Devolver código 500 si hay un error durante la eliminación


if __name__ == '__main__':
    app.run(debug=True)

