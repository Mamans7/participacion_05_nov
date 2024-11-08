from flask import Flask, request, url_for, render_template, redirect
import sqlite3
app = Flask(__name__)

# Creando la tabla
def creat_tabla():
  conectar = sqlite3.connect('almacen.db')
  conectar.execute(
    """
    create table if not exists producto(
      id integer primary key autoincrement,
      descripcion text not null,
      cantidad integer not null,
      precio real not null
    )
    """
  )
  conectar.commit()
  conectar.close()

@app.route('/')
def index():
  return render_template('index.html')

# AGREGANDO PARA PROBAR
# def agregar():
#   conectar = sqlite3.connect('almacen.db')
#   conectar.execute(
#     """
#     insert into producto(descripcion, cantidad, precio)
#     values('Choklo',24,12.5)
#     """
#   )
  conectar.commit()
  conectar.close()
# CREANDO LA TABLA
creat_tabla()
#agregar()

# LEYENDO DATOS DESDE LA BD almacen.db
@app.route('/productos')
def productos():
  conectar = sqlite3.connect('almacen.db')
  conectar.row_factory = sqlite3.Row
  cur = conectar.cursor()
  cur.execute('select * from producto')
  lista = cur.fetchall()
  return render_template('productos/index.html', lista=lista)

# AL DAR CLICK EN EL BOTON DE Nuevo
@app.route('/productos/crear')
def crear():
  return render_template('productos/crear.html')

# INSERTANDO REGISTROS
@app.route("/productos", methods=["POST"])
def produto_guardar():
  descripcion = request.form['descripcion']
  cantidad = request.form['cantidad']
  precio = request.form['precio']
  cone = sqlite3.connect('almacen.db')
  curso = cone.cursor()
  curso.execute("insert into producto(descripcion, cantidad, precio) values (?,?,?)",(descripcion, cantidad, precio))
  cone.commit()
  cone.close()
  return redirect('/productos')

# INSERTANDO FUNCIONALIDADES EN EL BOTON Editar
@app.route('/productos/editar/<int:id>')
def editar(id):
  cone = sqlite3.connect('almacen.db')
  cone.row_factory = sqlite3.Row
  curso = cone.cursor()
  curso.execute("select * from producto where id=?",(id,))
  prod = curso.fetchone()
  cone.close()
  return render_template("productos/editar.html",producto = prod)

# ACTUALIZAR PRODUCTOS  
@app.route("/productos/actualizar", methods=['POST'])
def actualizar_prod():
  id=request.form['id']
  descripcion = request.form['descripcion']
  cantidad = request.form['cantidad']
  precio = request.form['precio']
  cone = sqlite3.connect('almacen.db')
  curso = cone.cursor()
  curso.execute("UPDATE producto SET descripcion=?, cantidad=?, precio=? where id=?",(descripcion, cantidad, precio, id))
  cone.commit()
  cone.close()
  return redirect('/productos')

# PARA ELIMINAR PRODUCTOS
@app.route('/productos/eliminar/<int:id>')
def prod_eliminar(id):
  conn = sqlite3.connect("almacen.db")
  curso = conn.cursor()
  curso.execute("delete from producto where id=?",(id,))

  conn.commit()  
  conn.close()
  return redirect("/productos")

if __name__=='__main__':
  app.run(debug=True)