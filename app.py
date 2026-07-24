import os
'''import google.generativeai as genai'''
from flask import Flask, render_template
from flask import request, redirect, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from flask import send_file
from models.user import db, User
from models.task import Task
from datetime import date
import pandas as pd
from datetime import date
from flask import request, jsonify
from authlib.integrations.flask_client import OAuth
import secrets
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, session, flash, url_for

from flask import (
    send_file,
    jsonify
)

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret123"

app.config["JWT_SECRET_KEY"]="jwt-secret"

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///app.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    with app.app_context():

      admin = User.query.filter_by(
        email="admin@gmail.com"
       ).first()

    if admin:

        admin.is_admin = True
        db.session.commit()

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

#  GOOGLE OAUTH SETUP
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
#current user variable 
@app.context_processor
def inject_user():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return dict(current_user=user)
    return dict(current_user=None)

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        print("Entered Email:", email)

        user = User.query.filter_by(
            email=email
        ).first()

        print("User:", user)

        if user:
            print("Stored Hash:", user.password)

            result = check_password_hash(
                user.password,
                password
            )

            print("Password Match:", result)

        if user and check_password_hash(
                user.password,
                password):

            print("LOGIN SUCCESS")

            session["user_id"] = user.id
            session["is_admin"] = user.is_admin

            return redirect("/dashboard")

        print("LOGIN FAILED")

    return render_template("login.html")
@app.route('/login/google')
def google_login():
    # Yeh user ko Google ke login page par bhej dega
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    # Google se wapas aane ke baad data process karna
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    # Check karein agar user database mein pehle se hai
    user = User.query.filter_by(email=user_info['email']).first()
    
    if not user:
        # Naya user banayein (Password required hota hai, toh random de denge)
        random_password = secrets.token_hex(16)
        from werkzeug.security import generate_password_hash
        hashed_pw = generate_password_hash(random_password)
        
        user = User(name=user_info['name'], email=user_info['email'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        
    # User ko login karwa dein
    session['user_id'] = user.id
    flash('Successfully logged in with Google!', 'success')
    return redirect('/dashboard')   

@app.route("/register",  methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        print(name, email, password)

        hashed = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed
        )

        db.session.add(user)
        db.session.commit()

        print("User created successfully")

        return redirect("/")

    return render_template(
        "register.html"
    )



@app.route("/add_task", methods=["POST"])
def add_task():

    if "user_id" not in session:
        return redirect("/")

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    status = request.form["status"]
    due_date = request.form["due_date"]

    task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        due_date=due_date,
        user_id=session["user_id"]
    )

    db.session.add(task)
    db.session.commit()
    flash("Task added successfully!", "success")

    return redirect("/dashboard")

@app.route("/delete_task/<int:id>")
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()
    flash("Task deleted permanently.", "error")
    return redirect("/dashboard")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if 'user_id' not in session:
        return redirect('/login')
        
    task = Task.query.get(id)
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.status = request.form['status']
        task.due_date = request.form['due_date']
        db.session.commit()
        flash('Task successfully updated!', 'success')
        
        # User ko wahi bhejo jahan se wo aaya tha
        next_url = request.form.get('next', '/dashboard')
        return redirect(next_url)
        
    # GET request par 'next' url pakdo aur HTML mein bhejo
    next_url = request.args.get('next', '/dashboard')
    return render_template('edit_task.html', task=task, next_url=next_url)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    today_str = date.today().isoformat()
    search = request.args.get("search")
    filter_type = request.args.get("filter") # Naya filter parameter

    
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    # Stats logic (unchanged)
    total = Task.query.filter_by(user_id=session["user_id"]).count()
    pending = Task.query.filter_by(user_id=session["user_id"], status="Pending").count()
    completed = Task.query.filter_by(user_id=session["user_id"], status="Completed").count()
    in_progress = Task.query.filter_by(user_id=session["user_id"], status="In Progress").count()
    
    percentage = int((completed / total) * 100) if total > 0 else 0

    low = Task.query.filter_by(user_id=session["user_id"], priority="Low").count()
    medium = Task.query.filter_by(user_id=session["user_id"], priority="Medium").count()
    high = Task.query.filter_by(user_id=session["user_id"], priority="High").count()

    return render_template(
        "dashboard.html", tasks=tasks, total=total, pending=pending, 
        completed=completed, in_progress=in_progress, percentage=percentage, 
        low=low, medium=medium, high=high, today=today_str
    )

#  DRAG & DROP 
@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    task = Task.query.get_or_404(id)
    
    # Security check: User apna hi task edit kar raha hai
    if task.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    new_status = data.get("status")
    
    if new_status in ["Pending", "In Progress", "Completed"]:
        task.status = new_status
        db.session.commit()
        return jsonify({"success": True, "message": f"Task moved to {new_status}"})
    
    return jsonify({"error": "Invalid status"}), 400
@app.route(
    "/profile",
    methods=["GET","POST"]
)
def profile():

    if "user_id" not in session:
        return redirect("/")

    user = User.query.get(
        session["user_id"] )
    if user is None:
        session.clear()
        return redirect("/")

 #...user fetch
    if request.method == "POST":

        user.name = request.form["name"]
        user.email = request.form["email"]
        user.bio = request.form["bio"]
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                
                # File ko static/uploads mein save karna
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                
                # Database mein filename update karna
                user.profile_pic = filename
        db.session.commit()
        return redirect("/profile")

    return render_template(
        "profile.html",
        user=user
    )

@app.route("/export")
def export():

    if "user_id" not in session:
        return redirect("/")

    tasks = Task.query.filter_by(
        user_id=session["user_id"]
    ).all()

    data=[]

    for t in tasks:

        data.append({

            "Title":t.title,
            "Description":t.description,
            "Priority":t.priority,
            "Status":t.status,
            "Due Date":t.due_date


        })

    df = pd.DataFrame(data)

    file="tasks.xlsx"

    df.to_excel(
        file,
        index=False
    )

    return send_file(
        file,
        as_attachment=True
    )

@app.route("/users")
def users():

    users = User.query.all()

    for u in users:
        print(u.id, u.name, u.email, u.password)

    return "Check Terminal"

@app.route("/delete_photo")
def delete_photo():

    user = User.query.get(
        session["user_id"]
    )

    if user.profile_pic:

        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            user.profile_pic
        )

        if os.path.exists(path):
            os.remove(path)

        user.profile_pic = None
        db.session.commit()

    return redirect("/profile")

@app.route("/admin")
def admin():

    if not session.get("is_admin"):

        return redirect("/dashboard")

    total_users = User.query.count()

    total_tasks = Task.query.count()

    completed = Task.query.filter_by(
        status="Completed"
    ).count()

    users = User.query.all()

    return render_template(

        "admin.html",

        total_users=total_users,
        total_tasks=total_tasks,
        completed=completed,
        users=users
    ) 
@app.route("/calendar")
def calendar_view():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("calendar.html")

@app.route("/api/tasks")
def api_tasks():
    # Yeh route calendar ko events (tasks) JSON format mein dega
    if "user_id" not in session:
        return jsonify([])
    
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    events = []
    
    for task in tasks:
        # Status ke hisaab se color code
        color = "#198754" if task.status == "Completed" else ("#0d6efd" if task.status == "In Progress" else "#6c757d")
        if task.due_date < date.today().isoformat() and task.status != "Completed":
            color = "#dc3545" # Overdue (Red)

        events.append({
            "id": task.id,
            "title": task.title,
            "start": task.due_date,
            "color": color,
            "url": f"/edit_task/{task.id}?next=/calendar" # Click karne par edit page khulega
        })
        
    return jsonify(events)
@app.route("/delete_user/<int:id>")
def delete_user(id):

    if not session.get("is_admin"):

        return redirect("/dashboard")

    user = User.query.get(id)

    if user and user.id != session["user_id"]:

        Task.query.filter_by(
            user_id=id
        ).delete()

        db.session.delete(user)

        db.session.commit()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)