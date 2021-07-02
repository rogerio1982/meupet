from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import datetime
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/delete')
def dele():
   return render_template('delete.html')

@app.route('/enternew')
def new_student():
  now = datetime.now()
  data = now.today()
  hora = now.time()
  return render_template('add.html', data = data, hora = hora)

app.config["IMAGE_UPLOADS"] = join(dirname(realpath(__file__)), 'static')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':
      try:
       
        f = request.files['file']
        filename = secure_filename(f.filename)
        url = filename
        f.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
        print("Image saved")
        print(url)

        nm = request.form['nome']
        addr = request.form['descricao']
        city = "static/"+url
        pin = request.form['data']
         
        with sql.connect("database.db") as con:
          cur = con.cursor()
          cur.execute("INSERT INTO pet (nome,descricao,imagem,data) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
          con.commit()
          msg = "Inserido com sucesso!"
      except:
         con.rollback()
         msg = "Erro ao inserir!"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from pet order by data desc")
   
   rows = cur.fetchall();
   con.commit()
   return render_template("list.html",rows = rows)

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]

    with sql.connect("database.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from pet where id = ?",id)  
            con.commit()
            msg = "Removido com sucesso!"  
        except:  
            msg = "Erro ao deletar!"  
        finally:  
            return render_template("result.html",msg = msg)  

app.run(debug=True,host='0.0.0.0', port='8080')