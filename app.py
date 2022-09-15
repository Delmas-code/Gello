import os

# import app_main
from app_main import *
from flask import Flask, redirect, url_for, render_template, request, session, g, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

dirname = os.path.dirname(__file__)

app = Flask(__name__)

app.secret_key = 'goldenpixiebusinessforprofitofall'
app.config['UPLOAD_FOLDER'] = f"{dirname}/static/images"




user_name = ''

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


# Setting up a general function to handle all sessions of the uers


# Setting up a general function to handle all sessions of the uers


@app.before_request
def before_request():
    if 'username' in session:
        view_data = get_view()
        g.user = None
        # print(view_data)
        for x in view_data:
            # print(x)
            # print(f"<session>: {session['username']}")
            if x == session['username']:
                user = x
                g.user = user
                print("In the IF ")
    # print(g.user)
    
                


@app.after_request
def after_request(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/register/", methods=['GET', 'POST'])
def register():
    render_template('register.html')

@app.route("/login/", methods=['GET', 'POST'])
def login():
    
    global user_name
    if request.method == "POST":
        # first logs you out
        session.pop('username', None)
        # Gets usrname and pass from the form
        username = request.form['username']
        password = request.form['password']
        try:
            verify_usrname, verify_pass = com_login(username)
            #verify_pass contains the hashed password
            pass_verification = check_password_hash(verify_pass, password)
            print(pass_verification)
            if pass_verification:
                user_name = username 
                session['username'] = verify_usrname
                print(session)
                return redirect(url_for("dashboard"))
            else:
                # print("username or password is wrong")
                # flash('Wrong Username or Password', category="error")
                return render_template("login.html")
        except:
            flash('Wrong Username or Password', category="error")
            print("Wrong pass") 
            return render_template("login.html")
    
    else:
        return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not g.user:
        return redirect(url_for("login"))
    else:
        _company_info = company_info(g.user)
        ___ = _company_info[1]
        __ = ___.split("/")
        _image = os.path.join(f"{__[1]}/{__[2]}/{__[3]}")
        return render_template("dashboard.html", _name=_company_info[0], _image=_image, _email=_company_info[2])
    

@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        
        if 'file' not in request.files:
            return redirect(url_for("dashboard"))
        
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for("dashboard"))
        if file:
            # filename = secure_filename(file.filename)
            ext = file.filename
            ext_list = ext.split(".")
            filename = secure_filename(g.user)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/company_img", filename + "." + ext_list[1]))
        return redirect(url_for("dashboard"))
    

@app.route("/dashboard/profile", methods=['GET', 'POST'])
def profile():
    if not g.user:
        return redirect(url_for("login"))
    else:
        # _company_info = company_info(g.user)
        if request.method == "POST":
            # first logs you out
            # companyName = request.form['companyName']
            email = request.form['email']
            # dp = request.form['dp']
            phone = request.form['phone']
            
            c_pass = request.form['c_pass']
            n_pass = request.form['n_pass']
            con_pass = request.form['con_pass']
            verify_pass = com_login(g.user)[1]
            pass_verification = check_password_hash(verify_pass, c_pass)
            if pass_verification:
                if n_pass == con_pass:
                    update_company_info(conn, g.user, email, phone, con_pass)
                else:
                    return redirect(url_for("profile"))
            else:
                return redirect(url_for("profile"))
            
        _company_info = company_info(g.user)
        ___ = _company_info[1]
        __ = ___.split("/")
        _image = os.path.join(f"{__[1]}/{__[2]}/{__[3]}")
        return render_template("user-profile.html", _name=_company_info[0], _image=_image)


@app.route("/dashboard/coupons")
def coupons():
    return render_template("coupons.html")


@app.route("/contact-us")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run()
