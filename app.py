from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///menu.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "acedf"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route("/auth/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # flash("User already exists! Please login.", "error")
            return redirect(url_for("signup"))

        if not username or not password:
            flash("Missing username or password!", "error")
            return redirect(url_for("signup"))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))  

    return render_template("signup.html")  


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Missing username or password!", 400  
        
        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:
            return "Invalid username or password!", 401  
        
        login_user(user)
        return redirect(url_for("menu"))  
    return render_template("login.html") 

    
    
@app.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    session.clear() 
    return redirect(url_for("signup"))


@app.route("/")
def home():
    return redirect(url_for("signup"))

@app.route('/menu')
@login_required
def menu():
    items = MenuItem.query.all()
    return render_template("menu.html", items = items)


@app.route('/menu/add', methods=["POST"])
def add_item():
    name = request.form["name"]
    quantity = request.form["quantity"]

    new_item = MenuItem(name = name, quantity = int(quantity))
    db.session.add(new_item)
    db.session.commit()
    
    return redirect(url_for("menu"))


@app.route('/menu/edit/<int:item_id>')
def edit_item(item_id):
    item = MenuItem.query.get(item_id)
    return render_template("edit.html", item = item)

@app.route("/menu/update/<int:item_id>", methods=["POST"])
def update_item(item_id):
    item = MenuItem.query.get(item_id)
    item.name = request.form["name"]
    item.quantity = int(request.form["quantity"])

    db.session.commit()
    return redirect(url_for("menu"))

@app.route("/menu/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = MenuItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("menu"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
