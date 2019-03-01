from flask import Flask, render_template, request, redirect, session, flash
from mysqlconn import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
bcrypt = Bcrypt(app)

@app.route("/main")
def index():
    db= connectToMySQL('vacays')
    users = db.query_db('SELECT * FROM users;')
    userdata = users[0]
    print(users)
    return render_template("index.html", all_users = users, userdata = userdata)


    



@app.route("/create", methods=["POST"])
def create():
    is_valid = True		
    if len(request.form['full_name']) < 3:
        is_valid = False 
        flash("Please enter a name")
    
    if len(request.form['username']) < 3:
        is_valid = False
        flash("Please enter a valid username")
    
    if len(request.form['password']) < 8:
        flash("Please enter a valid password")

    if request.form['confirm'] != request.form['password']:
        is_valid = False
        flash("Password does not match")
    
    if is_valid==True:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        print(pw_hash) 
        query = "INSERT INTO users (full_name, username, password, created_at, updated_at) VALUES (%(n)s, %(un)s, %(pass_hash)s, NOW(), NOW());"
        data = {
            "n": request.form["full_name"],
            "un": request.form["username"],
            "pass_hash" : pw_hash.decode('utf-8')
        }
        db = connectToMySQL('vacays')
        flash("Successfully added")
        userdata = db.query_db(query,data)
        session['userdata'] = userdata
    
        return redirect("/travels")
    else:
        return redirect("/main")


# put log in info
            
@app.route("/travels")
def travels():
    # if 'userid' not in session:
    #     flash("you must log in")
    #     return redirect("/main")


    query = "SELECT * FROM users WHERE id=%(id)s;"
    data = {
        "id": session['userdata']

    }
    db = connectToMySQL('vacays')
    users = db.query_db(query, data)
    return render_template("travels.html", userdata=users[0])

            
@app.route("/main/travels/add")
def add_trip():
    return render_template("add_trip.html")

@app.route("/add", methods = ["POST"])
def add():
    #print request.form before second query see if it is going to add then print out form info and then do validations, if pass validations then create trip or redirect to redirect to form. 

    # query = "INSERT INTO travel_plan (destination, start_date, end_date, plan, created_at, updated_at) VALUES (%(d)s, %(sd)s, %(ed)s, %(plan)s, NOW(), NOW());"
    # data = {
    #     "d": request.form["destination"],
    #     "sd": request.form["start_date"],
    #     "ed": request.form["end_date"],
    #     "plan": request.form["plan"]
    # }
    # db = connectToMySQL('vacays')
    # userdata = db.query_db(query,data)
    # print(userdata)
    return redirect("/travels")
        


@app.route("/logout", methods=["POST"])
def logout():
    query = "SELECT * FROM users WHERE id=%(id)s;"

    data = {
        "id": session['userdata']
    }
    db = connectToMySQL('vacays')
    db.query_db(query, data)
    
    session.clear()
    return redirect("/main")








if __name__ == "__main__":
    app.run(debug=True)
