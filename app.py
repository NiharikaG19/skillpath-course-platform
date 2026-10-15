import os
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv(override=True)
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "replace-this-with-a-long-secret")
app.config.update(
    MYSQL_HOST=os.getenv("MYSQL_HOST", "localhost"),
    MYSQL_PORT=int(os.getenv("MYSQL_PORT", "3306")),
    MYSQL_USER=os.getenv("MYSQL_USER", "skillapp"),
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD", ""),
    MYSQL_DB=os.getenv("MYSQL_DB", "skill_course_db"),
    MYSQL_CURSORCLASS="DictCursor",
)
mysql = MySQL(app)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("target_role", "Data Analyst").strip() or "Data Analyst"
        if not name or not email or not password:
            flash("Please complete all required fields.", "danger")
            return render_template("register.html")
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return render_template("register.html")
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT id FROM users WHERE email=%s", (email,))
            if cur.fetchone():
                flash("That email already has an account. Please log in.", "warning")
                return redirect(url_for("login"))
            cur.execute("INSERT INTO users (name,email,password_hash,target_role) VALUES (%s,%s,%s,%s)",
                        (name,email,generate_password_hash(password),role))
            mysql.connection.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception:
            mysql.connection.rollback()
            app.logger.exception("Registration failed")
            flash("Registration failed. Check the VS Code terminal for the database error.", "danger")
        finally:
            cur.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT id,name,email,password_hash,target_role FROM users WHERE email=%s", (email,))
            user = cur.fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["target_role"] = user.get("target_role") or "Data Analyst"
                return redirect(url_for("dashboard"))
            flash("Email or password is incorrect.", "danger")
        finally:
            cur.close()
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id,title,provider,url,description,skill_name,difficulty FROM courses ORDER BY title")
        courses = cur.fetchall()
        cur.execute("SELECT id,task_name,completed,completed_at FROM progress WHERE user_id=%s ORDER BY id DESC",
                    (session["user_id"],))
        tasks = cur.fetchall()
        done_names = [t["task_name"].lower() for t in tasks if t["completed"]]
        recommended = [c for c in courses if not any((c.get("skill_name") or "").lower() in t for t in done_names)]
        total = len(tasks)
        completed = sum(bool(t["completed"]) for t in tasks)
        percentage = round(completed * 100 / total) if total else 0
        return render_template("dashboard.html", courses=courses, recommended_courses=recommended,
                               tasks=tasks, total=total, completed=completed, percentage=percentage)
    finally:
        cur.close()

@app.route("/progress/add", methods=["POST"])
@login_required
def add_progress():
    task = request.form.get("task_name", "").strip()
    if not task or len(task) > 200:
        flash("Enter a task of 1–200 characters.", "warning")
        return redirect(url_for("dashboard"))
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO progress (user_id,task_name,completed) VALUES (%s,%s,FALSE)",
                    (session["user_id"], task))
        mysql.connection.commit()
        flash("Task added.", "success")
    except Exception:
        mysql.connection.rollback()
        app.logger.exception("Adding task failed")
        flash("Could not add task.", "danger")
    finally:
        cur.close()
    return redirect(url_for("dashboard"))

@app.route("/progress/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_progress(task_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id,completed FROM progress WHERE id=%s AND user_id=%s",
                    (task_id, session["user_id"]))
        task = cur.fetchone()
        if task:
            state = not bool(task["completed"])
            cur.execute("""UPDATE progress SET completed=%s,
                completed_at=CASE WHEN %s THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE id=%s AND user_id=%s""", (state,state,task_id,session["user_id"]))
            mysql.connection.commit()
            flash("Progress updated.", "success")
        else:
            flash("Task not found.", "danger")
    except Exception:
        mysql.connection.rollback()
        app.logger.exception("Updating task failed")
        flash("Could not update progress.", "danger")
    finally:
        cur.close()
    return redirect(url_for("dashboard"))

@app.route("/progress/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_progress(task_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM progress WHERE id=%s AND user_id=%s", (task_id,session["user_id"]))
        mysql.connection.commit()
        flash("Task deleted.", "success")
    finally:
        cur.close()
    return redirect(url_for("dashboard"))

@app.route("/courses")
@login_required
def courses():
    q = request.args.get("q","").strip()
    cur = mysql.connection.cursor()
    try:
        if q:
            term = "%" + q + "%"
            cur.execute("""SELECT id,title,provider,url,description,skill_name,difficulty FROM courses
                           WHERE title LIKE %s OR provider LIKE %s OR skill_name LIKE %s ORDER BY title""",
                        (term,term,term))
        else:
            cur.execute("SELECT id,title,provider,url,description,skill_name,difficulty FROM courses ORDER BY title")
        return render_template("courses.html", courses=cur.fetchall(), search=q)
    finally:
        cur.close()

@app.route("/analytics")
@login_required
def analytics():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT COUNT(*) AS total,COALESCE(SUM(completed),0) AS completed FROM progress WHERE user_id=%s",
                    (session["user_id"],))
        stats = cur.fetchone()
        total = stats["total"] or 0
        completed = int(stats["completed"] or 0)
        percentage = round(completed*100/total) if total else 0
        cur.execute("SELECT skill_name,COUNT(*) AS course_count FROM courses GROUP BY skill_name ORDER BY skill_name")
        return render_template("analytics.html", total=total, completed=completed,
                               percentage=percentage, skill_stats=cur.fetchall())
    finally:
        cur.close()

if __name__ == "__main__":
    print("Starting SkillPath at http://127.0.0.1:5000")
    app.run(debug=True)
