from flask import Flask, render_template, request, redirect, session, flash, url_for
from mysqlconn import connectToMySQL
from flask_bcrypt import Bcrypt
import re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
bcrypt = Bcrypt(app)
now = str(datetime.now())

@app.route("/main")
def index():
    
    return render_template("index.html")


    



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
        print(userdata)
        print("*"*100)
        session['userdata'] = userdata
    
        return redirect("/travels")
    else:
        return redirect("/main")


@app.route("/login", methods=["POST"])
def login():
    db = connectToMySQL("vacays")
    query = "SELECT * from users WHERE username = %(un)s;"
    data = {
        "un": request.form["username"]
    }
    result = db.query_db(query,data)

    print(result)

    if len(result) == 0:
        flash("username not found, please register!")
        return redirect("/main")

    else:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']) == True:
            session['userdata'] = result[0]['id']
            return redirect("/travels")
        else:
            flash("Password does not match!")
            return redirect("/main")
            
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
    
    db = connectToMySQL('vacays')
    query = "SELECT * FROM users_travelplan RIGHT JOIN travel_plan ON travel_plan_id = %(id)s;"
   
    trips = db.query_db(query,data)
    # print(trips)
    print(users[0])

    return render_template("travels.html", userdata=users[0], trips=trips)

            
@app.route("/main/travels/add")
def add_trip():
    return render_template("add_trip.html")

@app.route("/add", methods = ["POST"])
def add():
    is_valid = True		
    if len(request.form['destination']) < 1:
        is_valid = False 
        flash("Please enter a Destination")
    
    if len(request.form['plan']) < 1:
        is_valid = False
        flash("Please enter a Description")
    
    if request.form['end_date'] < request.form['start_date']:
        is_valid = False
        flash("End date cannot come before start date!")


    if len(request.form['start_date']) < 1:
        is_valid = False
        flash("Please enter a travel date from")
    
    elif request.form['start_date'] < now:
        is_valid = False
        flash("Choose a different start date")
    
    if len(request.form['end_date']) < 1:
        is_valid = False
        flash("Please enter a Travel date to")
    
    elif request.form['end_date'] < now:
        is_valid = False
        flash("Choose a different end date")
    
    if is_valid == True:
        query = "INSERT INTO travel_plan (destination, start_date, end_date, plan, users_id, created_at, updated_on) VALUES (%(d)s, %(sd)s, %(ed)s, %(p)s, %(ud)s, NOW(), NOW());"
        data = {
            "d": request.form["destination"],
            "sd": request.form["start_date"],
            "ed" : request.form["end_date"],
            "p": request.form["plan"],
            "ud": session['userdata']
        }
        db = connectToMySQL('vacays')
        flash("Successfully added")
        tripdata = db.query_db(query,data)
        # print(tripdata)
        # print("*"*20)
        query = "INSERT INTO users_travelplan (users_id, travel_plan_id, created_at, updated_at) VALUES (%(ui)s, %(ti)s, NOW(), NOW());"
        data ={
            "ui": session["userdata"],
            "ti": tripdata
        }
        db = connectToMySQL('vacays')
        db.query_db(query,data)
        # print("%"*100)
        # print(db)

        # db = connectToMySQL('vacays')
        # query = "SELECT * FROM travel_plan WHERE id=%(id_num)s;"
        # data = {
        #     "ui": session["userdata"],
        #     "id_ num": 
        # }
        # tripdata = db.query_db(query, data)
        # print("*"*100)
        # print(tripdata)
        # print("*"*100)
        
        
        
        
        
        
        # db = connectToMySQL('vacays')
        # query = "SELECT * FROM travel_plan WHERE id=50;"
        # global testdata
        # testdata = db.query_db(query)
        # print("*"*100)
        # print(testdata)
        # print("*"*100)


        return redirect(url_for('travels'))
        # return redirect("/travels", testdata = testdata)

    else:
        return redirect("/main/travels/add")


@app.route("/main/travels/destination/<trip_id>")
def destination (trip_id):
    db = connectToMySQL("vacays")
    query = "select travel_plan.*, users.full_name from travel_plan Join users on travel_plan.users_id = users.id where travel_plan.id=%(trip_id)s;"
 
    # query= "Join users on travel_plan.users_id = users.id and users.id=%(trip_id)s;"
    # query =  "Join users on travel_plan.users_id = users.id and users.full_name= %(trip_id)s;"
    # query = "SELECT * FROM travel_plan where id = %(trip_id)s;"
    # query = "SELECT * FROM travel_plan, users where users_id = %(trip_id)s;"
    
    # query = "SELECT travel_plan.*, users.full_name FROM travel_plan, users where travel_plan.users_id = %(trip_id)s;"
    # query = "SELECT * FROM users join travel_plan where travel_plan_id = %(trip_id)s;"
    # query = "SELECT * FROM travel_plan join users where id = %(trip_id)s;"
    # query = "SELECT * FROM travel_plan RIGHT JOIN users on users_id = %(id)s;"
    # query = "SELECT * FROM users LEFT JOIN travel_plan on travel_plan_id = %(ti)s;"
    # query = "SELECT * FROM travel_plan join users on user_id = %(id)s;"

    data = {
        # "id": session['userdata'],
        "trip_id": trip_id,

    }
    
    trip= db.query_db(query,data)
    print("&"*100)
    print(trip)
    print("&"*100)

    return render_template("destination.html", trip = trip[0])



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
    # return redirect("/travels")
        


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
