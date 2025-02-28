from flask import Flask, flash, request, redirect,render_template, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, login_manager,login_required,login_user,logout_user


# importaciones .py
from config import Config
from models.entities.User import User
from models.ModelUser import ModelUser


app = Flask(__name__)

db = MySQL(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/login',  methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("hometienda"))
        else:
            return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(id,username,password,fullname="")

        logged_user = ModelUser.login(db,user)

        if logged_user:
            if logged_user.username == "admin":
                if logged_user.password:
                    login_user(logged_user)
                    return redirect(url_for("paneladmin"))
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for("hometienda"))
            else:
                flash("Contraseña incorrecta")
                return redirect(url_for("login"))
        else:
                flash("error al iniciar sesion")
                return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("hometienda"))
        else:
            return render_template("register.html")

    if request.method == "POST":
        fullname = request.form.get("fullname")
        password = request.form.get("password")
        username = request.form.get("username")

        user = User(id,username,password,fullname)

        ModelUser.register(db,username,password,fullname)

        logged_user = ModelUser.login(db,user) 
        if logged_user:
            login_user(logged_user)
            return redirect(url_for("hometienda"))
        else: 
            redirect(url_for("register"))

@app.route('/tiendahome', methods=["GET"])
@login_required
def hometienda():
    if request.method == "GET":
        return render_template("hometienda.html")
    
@app.route('/paneladmin')
@login_required
def paneladmin():
    if request.method == "GET":
        return render_template("paneladmin.html")
    

@app.route("/users", methods=["GET"])
@login_required
def users():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE not id = 1")
    users = cursor.fetchall()
    if request.method == "GET":
        return render_template("users.html", users=users)
@app.route("/delete/<id>")
def delete(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s",(id,))
    return redirect(url_for("users"))

@app.route("/productos", methods=["GET"])
@login_required
def productos():
    if request.method == "GET":
        return render_template("productos.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

def status_404(error):
    return "<h1>Pagina no encontrada😓<h1>"

def status_401(error):
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.config.from_object(Config["dev"])
    app.register_error_handler(404,status_404)
    app.register_error_handler(401,status_401)
    app.run()