from flask import Flask, render_template, request
import sqlite3 as sql
import smtplib
app = Flask(__name__)

@app.route('/')
def home():
   conn = sql.connect('database.db')
   conn.execute('CREATE TABLE if not EXISTS invited (uname TEXT, email TEXT)')
   conn.close()
   return render_template('home.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         uname = request.form['uname']
         email = request.form['email']

         with sql.connect("database.db") as con:


            con.execute('INSERT INTO invited VALUES (?,?)',(uname,email) )
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("isedept310@gmail.com", "isedept7")
            SUBJECT = "SNIPPT"
            TEXT = "Please visit this link \n www.mysnippt.com "
            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            server.sendmail("isedept310@gmail.com", email, msg)
            server.quit()
            msg = "Sent Invite,check mail. Thank you!!"
            con.commit()
      except :
         con.rollback()
         msg = "Try again"

      finally:
         return render_template("invites.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   rows=con.execute("select * from invited")
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
