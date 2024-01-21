from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv, find_dotenv
from marshmallow import fields, Schema
import os
import base64

# Lee la información existente en un archivo denominado .env
# Este es un archivo oculto en un servidor de producciómn y alberga
# las etiquetas y sus valores para la cadena de conexión a MongoDB

load_dotenv(find_dotenv())
usuario = os.environ.get("MYSQLDB_USUARIO")
password = os.environ.get("MYSQLDB_PASSWORD")
host = os.environ.get("MYSQLDB_HOST")
bd = os.environ.get("MYSQLDB_BD")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{usuario}:{password}@{host}/{bd}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hardsecretkey'  # Para las sesiones flash

db = SQLAlchemy(app)
ma = Marshmallow(app)

class GorraSchema(Schema):
    id = fields.Int()
    descripcion = fields.Str()
    stock = fields.Int()
    fecha_lanzamiento = fields.Date()
    nombre_imagen = fields.Str()
    imagen = fields.Method('get_imagen_base64')

    def get_imagen_base64(self, obj):
        if obj.imagen is not None:
            return base64.b64encode(obj.imagen).decode('utf-8')
        return None
