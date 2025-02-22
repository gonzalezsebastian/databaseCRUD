from flask import Flask, render_template, request, redirect, url_for, flash
import cx_Oracle
from DATA import db_user, db_password, db_dsn, db_encoding
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/hijo.html')
def hijo():
    
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        cursor = conn.cursor()
        cursor.execute("select * from hijo")
        data = cursor.fetchall()
        headings = [row[0] for row in cursor.description]
        conn.commit()
    
    return render_template("hijo.html", headings=headings, data=data)

@app.route('/create-hijo', methods=['POST'])
def create_hijo():
    
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        
        id_hijo = request.form['id_hijo']
        nombre_hijo = request.form['nombre_hijo']
        id_padre = request.form['id_padre']
        
        if id_padre == "":
            id_padre = "null"
        
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"INSERT INTO HIJO (ID, NOM, HIJODE) VALUES ({id_hijo}, '{nombre_hijo}', {id_padre})")
            conn.commit()
        except cx_Oracle.DatabaseError as e:
            pass
        finally:
            return redirect(url_for('hijo'))
        
@app.route('/deleteHijo/<id>')
def delete_hijo(id):
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"DELETE FROM HIJO WHERE ID={int(id)}")
            conn.commit()
        except cx_Oracle.DatabaseError as e:
            pass
        finally:
            return redirect(url_for('hijo'))



@app.route('/padre.html')
def padre():
    
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        cursor = conn.cursor()
        cursor.execute("select * from padre")
        data = cursor.fetchall()
        headings = [row[0] for row in cursor.description]
        conn.commit()
    
    return render_template("padre.html", headings=headings, data=data)

@app.route('/create-padre', methods=['POST'])
def create_padre():
    print('hola')
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        
        id_padre = request.form['id_padre']
        nombre_padre = request.form['nombre_padre']
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"INSERT INTO PADRE (ID, NOM) VALUES ({id_padre}, '{nombre_padre}')")
            conn.commit()
        except cx_Oracle.DatabaseError as e:
            print(e)
            print("error")
            pass
        finally:
            return redirect(url_for('padre'))

@app.route('/deletePadre/<id>')
def delete_padre(id):
    
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"DELETE FROM PADRE WHERE ID={int(id)}")
            conn.commit()
        except cx_Oracle.DatabaseError as e:
            print(e)
            print("Hubo error")
            pass
        finally:
            return redirect(url_for('padre'))

@app.route('/consulta1.html')
def consulta1():
    return render_template("consulta1.html")

@app.route('/show-hijos', methods=['POST'])
def show_hijos():
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        
        id_padre = request.form['id_padre']
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"select id,nom from hijo where hijode={int(id_padre)}")
            data = cursor.fetchall()
            headings = [row[0] for row in cursor.description]
            conn.commit()
            if data:
                return render_template('consulta1.html', data=data, headings=headings)
            else:
                return render_template('consulta1.html', message="Este padre no tiene hijos, o no existe un padre con ese ID")
        except Exception as e:
            return render_template('consulta1.html', message="No hay un padre con ese ID, o usted ingresó un ID invalido")

@app.route('/consulta2.html')
def consulta2():
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        cursor = conn.cursor()
        cursor.execute("select padre.id, padre.nom from padre left outer join hijo on padre.id = hijo.hijode where hijo.hijode is null")
        data = cursor.fetchall()
        headings = [row[0] for row in cursor.description]
    
    return render_template("consulta2.html", headings=headings, data=data)

@app.route('/consulta3.html')
def consulta3():
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        cursor = conn.cursor()
        cursor.execute("select id, nom, nvl(to_char(hijode),'no tiene') as padre from hijo where hijode is null")
        data = cursor.fetchall()
        headings = [row[0] for row in cursor.description]
    
    return render_template("consulta3.html", headings=headings, data=data)

@app.route('/consulta4.html')
def consulta4():
    with cx_Oracle.connect(
            user=db_user,
            password=db_password,
            dsn=db_dsn,
            encoding=db_encoding
        ) as conn:
        cursor = conn.cursor()
        cursor.execute("select padre.id, padre.nom, count(hijo.hijode) as cantidad from padre, hijo where padre.id=hijode group by padre.id, padre.nom order by cantidad desc")
        data = cursor.fetchall()
        headings = [row[0] for row in cursor.description]
    
    return render_template("consulta4.html", headings=headings, data=data)