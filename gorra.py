from database import db
from sqlalchemy.sql import func

# Para crear las tablas, desde el entorno de ejecución de Python, ejecutar:
# from database import app, db
# from gorra import Gorra
# app.app_context().push()
# db.create_all()

class Gorra(db.Model):
    
    __tablename__ = 'gorras'
         
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    fecha_lanzamiento = db.Column(db.Date)
    nombre_imagen = db.Column(db.String(100))
    imagen = db.Column(db.LargeBinary)
     
    def __init__(self, descripcion, stock, fecha_lanzamiento, nombre_imagen, imagen):
        self.descripcion = descripcion
        self.stock = stock
        self.fecha_lanzamiento = fecha_lanzamiento
        self.nombre_imagen = nombre_imagen
        self.imagen = imagen

    def __repr__(self):
        return f'<Gorra {self.id}>: {self.descripcion}'
    
    