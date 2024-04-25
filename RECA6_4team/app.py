import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# main login page
@app.route("/")
@login_required
def index():
    """Show article list per user"""
    return render_template("index.html")



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


@app.route("/logout")
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
        flash("Register")
        return render_template("register.html")

# 권한 함수
@app.route("/private", methods=["POST"])
def private():
    # 세션에 사용자가 있는지 확인
    if "user_name" in session:
        username = session["user_name"]
        # 요청된 사용자 이름과 세션의 사용자 이름이 일치하는지 확인
        requested_username = request.form.get("username")
        if username == requested_username:
            # 권한이 있으면 특정 작업 수행
            flash("You have permission to access this page.")
            # edit ..
            # delete ..
        else:
            # 권한이 없으면 메세지 출력
            flash("You do not have permission to access this page.")
    else:
        # 세션이 없으면 게스트로 플래시
        flash("You are accessing as a guest.")
        return redirect(url_for("guest"))
    return redirect(url_for("index"))

# create 함수
@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        # 사용자가 로그인한 경우
        if "user_name" in session:
            username = session["user_name"]
            # 사용자에게 블로그 제목을 입력 받음
            blog_title = request.form.get("blog_title")

            # 블로그 제목을 데이터베이스에 추가
            db.execute("INSERT INTO blogs (username, title) VALUES(?, ?)", username, blog_title)

            # 새로운 HTML 파일 생성
            # 여기에서 새로운 HTML 파일을 생성하는 코드를 추가해야 함

            # 새로운 HTML 파일의 주소 반환
            html_address = f"/blogs/{username}/{blog_title}.html"
            return redirect(html_address)
        # 권한이 없으면 나가리
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))
    else:
        return render_template("create.html")
