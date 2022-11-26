from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
app.secret_key='a';  


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zyy94826;PWD=Ryzzy2HporAlyl2F",'','')
print("connection")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])   
def login():  
    global userid
    msg=''

    if request.method == 'POST':
        username=request.form['firstname']
        password=request.form['password']
        sql=f"SELECT * FROM user WHERE firstname=?{username} AND {password}";
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        res=ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if res:
            session['loggedin']=True
            session['id']=account['USERNAME']
            userid=account['USERNAME'] 
            session['username']=account['USERNAME']
            return render_template('dashboard.html', msg = msg)
        else:
            msg='incorrect id/password'
    return render_template('login.html',msg=msg)    

    
#######################################################

@app.route('/sign',methods=['GET','POST'])
def sign():
    msg = ''
    if request.method == 'POST' :
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'passwrod must contain characters and numbers !'
        else:
            insert_sql = "INSERT INTO  user VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, firstname)
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('sign.html', msg = msg)

##################################
@app.route('/recur',methods=["GET","POST"])
def recur():

    if request.method == "POST":
        companyname = request.form.get("companyname")
        designation = request.form.get("designation")
        qualification = request.form.get("qualification")
        skills = request.form.get("skills")
        batch = request.form.get("batch")
        location = request.form.get("location")
        bucket='resumes-storage'
        file_name=request.form.get("email")
        file=request.files("resume")
       
        sql = "INSERT INTO JOBSLIST VALUES (?,?,?,?,?,?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, companyname)
        ibm_db.bind_param(stmt, 2, designation)
        ibm_db.bind_param(stmt, 3, qualification)
        ibm_db.bind_param(stmt, 4, skills)
        ibm_db.bind_param(stmt, 5, batch)
        ibm_db.bind_param(stmt, 6, location)
        ibm_db.execute(stmt)
        print("job posted successfully")

    return render_template("recur.html")

@app.route('/about')
def about():
   return render_template('about.html')

###################


if __name__ =='__main__':  
    app.run(debug = True) 



