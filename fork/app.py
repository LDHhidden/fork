import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
# 구 - sqlite3는 추가하고 usd 지웠습니다. 이외에도 필요없는 라이브러리는 import안해도 될 듯 합니다
from helpers import apology, login_required, lookup
import sqlite3

# Flask On
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

# That use only cache information
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# main login page #구- likes항목 추가
@app.route("/")
# @login_required
def index():
    data = db.execute("SELECT title,user_id,datetime,likes FROM article")
    print(data)
    return render_template("index.html",data=data)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout",methods=["GET","POST"])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if password == "" or confirmation == "" or username == "":
            return apology("Input all fields")
        if not (password == confirmation):
            return apology("Password and Confirmation do not match")

        user = db.execute("SELECT * FROM users WHERE username=?", username)

        if len(user) == 1:
            return apology("Username already exists")
        else:
            hashpass = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashpass)

        return redirect("/")

    else:
        return render_template("register.html")

# 권한 함수 #구-likes 항목 추가
@app.route("/private", methods=["GET","POST"])
def private():
    # 세션 존재 여부
    id = session["user_id"]
    data = db.execute("SELECT user_id,title,datetime,likes FROM article where user_id=?",id)
    return render_template("private.html",data=data)

    # return render_template("private.html")

# edit_blog.html -> private.html
@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method == "GET":
        id = request.form.get("id")
        title = request.form.get("title")
        contents = request.form.get("contents")
        print(id)
        print(title)
        print(contents)
        db.execute("UPDATE article SET title=?, contents=? WHERE id=?",title,contents,id)
        return redirect("/private")
    else:
        return render_template("/edit_blog.html")

# create 함수
@app.route("/create", methods=["GET", "POST"])
# @login_required
def create():
    if request.method == "POST":
        id = session["user_id"]
        title = request.form.get("title")
        data = request.form.get("editordata")
        db.execute("INSERT INTO article(user_id,title,contents) VALUES (?,?,?)",id,title,data)
        return redirect("/private")
        
    else:
        return render_template("edit_blog.html")

@app.route("/delete",methods=["GET","POST"])
def delete():
    if request.method == "GET": 
        title = request.args.get("title")
        db.execute("DELETE FROM article WHERE title=?",title)
        return redirect("/private")
    else:
        return redirect("/private")

#구- likes항목 추가
@app.route("/view", methods=["GET","POST"])
def view():
    # id = session["user_id"]
    # title = db.execute("SELECT title FROM article where user_id=?",id)
    title = request.args.get("title")
    data = db.execute("SELECT contents,datetime,likes FROM article where title=?",title)
    print(data)
    return render_template("view.html",title=title,contents=data[0]["contents"],datetime=data[0]["datetime"],likes=data[0]["likes"])

@app.route("/update",methods=["GET","POST"])
def update():
    if request.method == "GET": 
        title = request.args.get("title")
        data=db.execute("SELECT id,title,contents FROM article WHERE title=?",title)
        print(data[0]["id"])
        return render_template("blog_edit.html",id=data[0]["id"],title=data[0]["title"],content=data[0]["contents"])
    else:
        return redirect("/private")

#구 - 좋아요 버튼 시작
# @app.route('/')
# def home():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM ARTICLE")
#     articles = c.fetchall()
#     conn.close()
#     return render_template('private.html', data=articles)

# @app.route('/like/<int:article_id>')
# def like_article(article_id):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute("UPDATE ARTICLE SET likes = likes + 1 WHERE id = ?", (article_id,))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('private'))
# #구 - 좋아요 버튼 끝