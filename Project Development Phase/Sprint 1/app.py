from flask import Flask, render_template
import ibm_db
import re

app = Flask(__name__)
app.secret_key='a';  


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')   
def login():
    return render_template("login.html")  

           

@app.route('/sign')
def sign():
    return render_template("sign.html")

@app.route('/recur')
def recur():
    return render_template("recur.html")

@app.route('/about')
def about():
   return render_template('about.html')



if __name__ =='__main__':  
    app.run(debug = True) 



