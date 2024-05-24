from flask import Flask, render_template, request, session, redirect, url_for
from pyclub.dbconnect import *
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = 'XoGaQ-Ae.(W8pt9=5[_ZF6mkE]8%;VM+]@saRZ4Ag'

#main page with login
@app.route("/",methods = ["POST"])
def login_page():
    error_message = None
    if request.method == "POST":
        login = request.form['login']
        passwd = request.form['password']
        if login and passwd :
            if login_user(login,passwd):#do dodania - funkcja ktora zaloguje i zwroci boolean
                session["username"] = login
        else:
            error_message = "Błąd wprowadzonych danych"
    return render_template("index.html",error=error_message)

@app.route("/register/", methods = ["POST"])
def register_page():
    error_message = None
    if request.method == "POST":
        new_username = request.form['login']
        new_password = request.form['password']
        new_password_confirm = request.form['password_confirm']

        if new_username and new_password and new_password == new_password_confirm:
            new_password_hash = generate_password_hash(new_password)
            create_user(new_username, new_password_hash) #funkcja rejestrująca
        elif new_password != new_password_confirm:
            error_message = "Hasła muszą się zgadzać"
        else:
            error_message = "Uzupełnij wszystkie pola"
    return render_template("register.html", error = error_message)
@app.route("/rating/")
def show_rating():
    if session["name"] == None
        return redirect(url_for('index'))
    else:
        players = get_top10_players() #dododania funkcja zczytująca pierwsze 10 graczy
        return render_template("ranking.html",players_list = players)

@app.route('/places/')
def show_places():
    if session["name"] == None
        return redirect(url_for('index'))
    else:
        places = get_places_list() # lista obiektów klasy Place
        return render_template('places.html', places_list = places)

@app.route('/place/<place_id>/') #do przemyslenia
def show_place(place_id):
    if session["name"] == None
        return redirect(url_for('index'))
    else:
        place = get_place(place_id)
        name = place.get_name()
        address = place.get_address()
        description = place.get_descr()
        points = place.get_points()
        gps_lon = place.get_lon()
        gps_lat = place.get_lat()
        discovery = get_discovery(place_id) #boolean sprawdza czy discovery dla uzytkownika jest w bazie
        if request.method == "POST":
            code = request.form(unlock_code)
            unlock_place(code, place_id)
        if discovery:
            return render_template('place.html', place_name=name, place_address = address, points_value = points ,gps_lon_value = gps_lon,gps_lat_value = gps_lat, place_description = description)
        else:
            return render_template('place-hidden.html', place_name=name, place_address=address, place_description = description)



@app.route('/place/<place_id>/comments')
def show_comments(place_id):
    if session["name"] == None
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            new_comment = request.form["comment_content"]
            add_comment(new_comment)
        comments = get_comments(place_id)
        return render_template('comment.html', comments_list = comments)

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))
