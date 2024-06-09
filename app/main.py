from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dbconnect import *
from user import User
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'XoGaQ-Ae.(W8pt9=5[_ZF6mkE]8%;VM+]@saRZ4Ag'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Zaloguj się aby uzyskać dostęp"

@login_manager.user_loader
def load_user(key):
    print(key)
    return get_user_by_id(key)

#main page with login
@app.route("/", methods = ["POST", "GET"])
def login_page():
    error_message = None
    if request.method == "POST":
        login = request.form['login']
        passwd = request.form['password']
        user_dict = get_user(str(login))
        if user_dict is None:
            error_message = "Brak użytkownika o podanym loginie"
        else:
            if check_password_hash(user_dict['password'], passwd):
                login_user(user_dict)
                flash("Poprawnie zalogowano")
                session["name"] = login
                return redirect(url_for('show_places'))
            else:
                error_message = "Błąd wprowadzonych danych"
    return render_template("index.html",error=error_message)

@app.route("/register/", methods = ["POST", "GET"])
def register_page():
    error_message = None
    if request.method == "POST":
        new_username = request.form['login']
        new_email = request.form['email']
        new_password = request.form['password']
        new_password_confirm = request.form['password_confirm']

        if new_username and new_password and new_password == new_password_confirm and '@' in new_email:
            new_password_hash = generate_password_hash(new_password)
            error_message = create_user(new_username, new_email, new_password_hash) #funkcja rejestrująca
            return redirect(url_for("login_page"))
        elif new_password != new_password_confirm:
            error_message = "Hasła muszą się zgadzać"
        elif '@' not in new_email:
            error_message = "Niepoprawny adres email"
        else:
            error_message = "Uzupełnij wszystkie pola"
    return render_template("register.html", error = error_message)

@app.route("/rating/")
@login_required
def show_rating():
    if session["name"] == None:
        return redirect(url_for('index'))
    else:
        players = get_top10_players() #dododania funkcja zczytująca pierwsze 10 graczy
        return render_template("ranking.html",players_list = players)

@app.route('/places/')
@login_required
def show_places():
    if session["name"] == None:
        return redirect(url_for('index'))
    else:
        places = get_places_list() # lista obiektów klasy Place
        return render_template('places.html', places_list = places)

@app.route('/place/<place_id>/', methods = ["POST", "GET"])
@login_required
def show_place(place_id):
    error_message = None
    if session["name"] == None:
        return redirect(url_for('index'))
    else:
        place = get_place(place_id)
        discovery = get_discovery(current_user.get_id(), place_id) #boolean sprawdza czy discovery dla uzytkownika jest w bazie
        if request.method == "POST":
            unlock_code = request.form['unlock_code']
            error_message = unlock_place(unlock_code, place_id, current_user.get_id())
            if error_message:
                return render_template('place-hidden.html', place_dict=place, error=error_message)
            return redirect(url_for('show_places'))
        elif discovery is None:
            return render_template('place-hidden.html', place_dict=place)
        comments = get_comments(place_id)
        return render_template('place.html', place_dict=place, discovery_date=discovery, comments_dict=comments)

@app.route('/place/<place_id>/add_comment', methods = ["POST"])
@login_required
def add_comments(place_id):
    if session["name"] == None:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            new_comment = request.form["comment_content"]
            add_comment(new_comment, place_id, current_user.get_id())
        else:
            return redirect(url_for('show_places'))
        return redirect(url_for('show_places'))

@app.route('/logout')
@login_required
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = "8080", debug="True")