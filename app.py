from flask import Flask, render_template, redirect, url_for, request, session
import os
import subprocess

app = Flask(__name__)
# os.urandom(24) generated key
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
information = {}
def register_with_user_info(uname, pword, twofa):
    if uname not in information:
        information[uname] = [pword, twofa]
        return 0
    else:
        return 1
def login_with_user_info(uname, pword, twofa):
    if uname not in information:
        return 2
    if pword != information[uname][0]:
        return 2
    if twofa != information[uname][1]:
        return 1
    return 0

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    success = ""
    if 'username' not in session:
        if request.method == 'POST':
            uname = request.form['uname']
            pword = request.form['pword']
            twofa = request.form['2fa']
            status = register_with_user_info(uname, pword, twofa)
            if status == 0:
                success = "Registration Success!"
            else:
                success = "Registration Failure!"
        return render_template("register.html", id = success)
    else:
        success = "Already logged in!"
        return render_template("register.html", id = success)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    result = ""
    if 'username' not in session:
        if request.method == 'POST':
            uname = request.form['uname']
            pword = request.form['pword']
            twofa = request.form['2fa']
            status = login_with_user_info(uname, pword, twofa)
            if status == 2:
                result = "Incorrect username or password!"
            elif status == 1:
                result = "Two-factor failure!"
            else:
                result = "Success!"
                session['username'] = uname
        return render_template("login.html", id = result)
    else:
        result = "Already logged in!"
        return render_template("login.html", id = result)

@app.route("/spell_check", methods = ['GET', 'POST'])
def spell_check():
    if 'username' in session:
        textout = ""
        misspelled = ""
        if request.method == 'POST':
            textout = request.form['inputtext']
            with open("test.txt", "w+") as fo:
                fo.write(textout)
            misspelled = subprocess.check_output(["./a.out", "test.txt", "wordlist.txt"])
            fo.close()
            os.remove("test.txt")
        return render_template("spell_check.html", textout = textout, misspelled = misspelled)
    else:
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()


