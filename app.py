from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import app, db, GorraSchema
from gorra import Gorra
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
from base64 import b64encode
import os

# Creamos los esquemas de Marshmallow
gorra_schema = GorraSchema()
gorras_schema = GorraSchema(many=True)

# Definimos la ruta principal de la aplicación
@app.route('/')
def home():
    gorras = Gorra.query.all()
    gorrasLeidas = gorras_schema.dump(gorras)
    return render_template('index.html', gorras = gorrasLeidas)

# Definimos la ruta para crear una nueva gorra
@app.route('/create', methods=['GET', 'POST'])
def createGorra():
    form = GorraForm()
    if form.validate_on_submit():
        descripcion = form.descripcion.data
        stock = form.stock.data
        fecha_lanzamiento = form.fecha_lanzamiento.data
        nombre_imagen = form.nombre_imagen.data
        imagen = form.imagen.data

        imagen_path = os.path.join('/tmp', secure_filename(imagen.filename))
        imagen.save(imagen_path)

        with open(imagen_path, 'rb') as f:
            imagen_bin = f.read()

        nueva_gorra = Gorra(descripcion, stock, fecha_lanzamiento, nombre_imagen, imagen_bin)
        db.session.add(nueva_gorra)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_gorra.html', form=form)

# Definimos la ruta para eliminar una gorra
@app.route('/delete', methods=['GET', 'POST'])
def deleteGorra():
    if request.method == 'POST':
        id = request.form['id']
        gorra = Gorra.query.get(id)
        if gorra:
            db.session.delete(gorra)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('delete_gorra.html', error='El ID introducido no existe')
    else:
        return render_template('delete_gorra.html')

# Definimos la ruta para editar una gorra
@app.route('/edit/<id>', methods=['GET', 'POST'])
def editGorra(id):    
    gorra = Gorra.query.get(id)
    if gorra is None:
        return notFound()

    form = EditGorraForm(obj=gorra)
    imagen_base64 = b64encode(gorra.imagen).decode('utf-8') if gorra.imagen else None
    
    if form.validate_on_submit():
        gorra.descripcion = form.descripcion.data
        gorra.stock = form.stock.data
        gorra.fecha_lanzamiento = form.fecha_lanzamiento.data
        gorra.nombre_imagen = form.nombre_imagen.data

        # Guardar la imagen en la base de datos como datos binarios
        imagen = request.files['imagen']
        if imagen.filename != '':
            imagen_filename = secure_filename(gorra.nombre_imagen) + '.' + imagen.filename.rsplit('.', 1)[1].lower()
            imagen_path = os.path.join('/tmp', imagen_filename)
            imagen.save(imagen_path)
            with open(imagen_path, 'rb') as f:
                gorra.imagen = f.read()

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_gorra.html', form=form, imagen_base64=imagen_base64)

# Definimos los formularios para crear y editar gorras
class EditGorraForm(FlaskForm):
    descripcion = StringField('Descripcion', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    fecha_lanzamiento = DateField('Fecha de Lanzamiento', validators=[DataRequired()])
    nombre_imagen = StringField('Nombre de la Imagen', validators=[DataRequired()])
    imagen = FileField('Imagen', validators=[DataRequired()])

class GorraForm(FlaskForm):
    descripcion = StringField('Descripcion', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    fecha_lanzamiento = DateField('Fecha de Lanzamiento', format='%Y-%m-%d', validators=[DataRequired()])
    nombre_imagen = StringField('Nombre de la Imagen', validators=[DataRequired()])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Crear Gorra')

# Manejo de errores para el error 404
@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
