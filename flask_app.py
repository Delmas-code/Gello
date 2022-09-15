import os
# import app_main
# from app_main import *
from flask import Flask, redirect, url_for, render_template, request, session, g, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


dirname = os.path.dirname(__file__)

app = Flask(__name__)

app.secret_key = 'goldenpixiebusinessforprofitofall'
app.config['UPLOAD_FOLDER'] = f"{dirname}/static/images"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/gelloData.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

_product_clicked= ''


#create a Company model
class Companies(db.Model, UserMixin):
    
    image = db.Column(db.String(100))
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, name, email, password_hash, phone, image):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.image = image
    def get_id(self):
        return (self._id)
    

    
#Creating the Coupons Model
    
class Coupons(db.Model):
    
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    discount = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    products = db.relationship('Products', backref='coupons')

    
    def __init__(self, name, discount, company, products):
        self.name = name
        self.company = company
        self.discount = discount
        self.products = products
        
    def get_id(self):
        return (self._id)
    
    
#create a Product model
class Products(db.Model):

    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100))
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    feature_image = db.Column(db.String(100))
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'))

    def __init__(self, name, price, status, image, company, description, feature_image, coupon_id=0):
        self.name = name
        self.price = price
        self.status = status
        self.image = image
        self.company = company
        self.description = description
        self.feature_image = feature_image
        self.coupon_id = coupon_id

    def get_id(self):
        return (self._id)
    
        
#Instantiates the class login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Load User whwen we log in
@login_manager.user_loader
def load_company(company_id):
    return Companies.query.get(int(company_id))
        
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/shop")
def shop():
    _products = Products.query.all()
    _companies = Companies.query.all()
    product_names = []
    product_prices = []
    product_images = []
    product_status = []
    product_companies  = []
    companies=[]

    # _products = Products.query.filter_by(name=current_user.name).all()

    for _product in _products:
        product_names.append(_product.name)
        product_prices.append(_product.price)
        product_images.append(_product.image)
        product_companies.append(_product.company)
        if _product.status == 'yes':
            product_status.append('In Stock')
        else:
            product_status.append('Out of Stock')
    for company in _companies:
        companies.append(company.name)
            
    return render_template("shop.html", product_names=product_names, product_prices=product_prices, product_images=product_images, product_status=product_status, product_companies=product_companies, companies=companies)

@app.route("/companies/<name>")
def company_page(name):
    product_names = []
    product_prices = []
    product_images = []
    product_status = []
    product_companies = []
    companies = []

    company_products = Products.query.all()
    _companies = Companies.query.all()

    for _product in company_products:
        if _product.company == name:
            product_names.append(_product.name)
            product_prices.append(_product.price)
            product_images.append(_product.image)
            product_companies.append(_product.company)
            if _product.status == 'yes':
                product_status.append('In Stock')
            else:
                product_status.append('Out of Stock')
                
    for company in _companies:
        companies.append(company.name)
        
    return render_template("company_page.html", product_names=product_names, product_prices=product_prices, product_images=product_images, product_status=product_status, product_companies=product_companies, companies=companies)

@app.route("/product/<name>")
def product(name):
    _product = Products.query.filter_by(name=name).first()
    _product_clicked = name

    return render_template("single.html", p_name=_product.name, p_price=_product.price, p_description=_product.description, p_company=_product.company, p_status=_product.status, p_image=_product.image, p_f_image=_product.feature_image)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        image = 'images/company_img/AfriGaz_9.jpg'
        
        password_hash = generate_password_hash(password)
        check_email = Companies.query.filter_by(email=email).first()
        if check_email:
            flash("Email Already Exist")
            return redirect(url_for("register"))
        else:
            company = Companies(username, email, password_hash, phone, image)
            db.session.add(company)
            db.session.commit()
            return redirect(url_for("login")) 
    return render_template("register.html")

                  

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember_me') else False
        company = Companies.query.filter_by(name=username).first()
        if company:
            #Check hash password
            if check_password_hash(company.password_hash, password):
                login_user(company, remember=remember)
                return redirect(url_for("dashboard"))
            else:
                flash('Wrong Password')
                return redirect(url_for("login"))
        else:
            flash("Company Doesn't exist")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")
    


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete_account():
    Products.query.filter_by(company=current_user.name).delete()
    Companies.query.filter_by(name=current_user.name).delete()
    db.session.commit()
    print("deleted")
    return redirect(url_for("index"))
    
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You've been logged out")
    return redirect(url_for("login")) 

@app.route("/dashboard")
@login_required
def dashboard():
    _name= current_user.name
    _email=current_user.email
    _image=current_user.image
    
    product_names = []
    product_prices = []
    product_images = []
    product_status = []
    
    # company = Companies.query.filter_by(name=current_user.name).first()
    company_products = Products.query.all()
    # _products = Products.query.filter_by(name=current_user.name).all()
    print(company_products)
    
    for _product in company_products:
        if _product.company == current_user.name:
            product_names.append(_product.name)
            product_prices.append(_product.price)
            product_images.append(_product.image) 
            if _product.status == 'yes':
                product_status.append('In Stock')
            else:
                product_status.append('Out of Stock')
    
    print(product_images) 
    return render_template("dashboard.html", _name=_name, _email=_email, _image=_image, product_names=product_names, product_prices= product_prices, product_images=product_images, product_status= product_status)


@app.route("/profile_uploader", methods=['GET', 'POST'])
@login_required
def profile_uploader():
    if request.method == "POST":
        company = Companies.query.filter_by(name=current_user.name).first()
        email = request.form['email']
        # dp = request.form['dp']
        phone = request.form['phone'] 
        company.email = email
        company.phone = phone
        db.session.commit()


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

            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'] + "/company_img", filename + "." + ext_list[1]))
        return redirect(url_for("dashboard"))


@app.route("/dashboard/profile", methods=['GET', 'POST'])
@login_required
def profile():
    _name = current_user.name
    _email = current_user.email
    _image = current_user.image
    
    if request.method == "POST":
        # companyName = request.form['companyName']
        company = Companies.query.filter_by(name=current_user.name).first()
        o_pass = request.form['c_pass']
        n_pass = request.form['n_pass']
        con_pass = request.form['con_pass']
        if check_password_hash(current_user.password_hash, o_pass):
            password_hash = generate_password_hash(n_pass)
            company.password_hash = password_hash
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("user-profile.html", _name=_name, _email=_email, _image=_image)


@app.route("/product_uploader", methods=['GET', 'POST'])
@login_required
def product_uploader():
    if request.method == "POST":
        product_name = request.form['productName']
        product_price = request.form['price']
        product_description = request.form['description']
        


        if ('p_image' not in request.files) and ('f_image' not in request.files):
            pass

        p_image = request.files['p_image']
        f_image = request.files['f_image']
        if p_image.filename == '' and f_image.filename == '':
            pass
        if p_image:
            # filename = secure_filename(file.filename)
            ext = p_image.filename
            ext_list = ext.split(".")
            filename = secure_filename(product_name)
            p_image_path = f"images/product_img/{filename}.{ext_list[1]}"
            
            p_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'] + "/product_img", filename + "." + ext_list[1]))
        if f_image:
            # filename = secure_filename(file.filename)
            ext = f_image.filename
            ext_list = ext.split(".")
            filename = secure_filename(product_name) 
            f_image_path = f"images/feature_img/{filename}.{ext_list[1]}"
            p_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'] + "/feature_img", filename + "." + ext_list[1]))
            
        new_product = Products(name=product_name,
                               price=product_price,
                               image=p_image_path,
                               description=product_description,
                               status='yes',
                               company=current_user.name,
                               feature_image=f_image_path)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route("/dashboard/add_product",  methods=['GET', 'POST'])
@login_required
def add_products():
    _name = current_user.name
    _email = current_user.email
    _image = current_user.image
    
    return render_template("add_products.html", _name=_name, _email=_email, _image=_image)


@app.route("/product_editter", methods=['GET', 'POST'])
@login_required
def product_editter():
    if request.method == "POST":
        product_name = request.form['productName']
        product_price = request.form['price']
        product_description = request.form['description']

        if ('p_image' not in request.files) and ('f_image' not in request.files):
            pass

        p_image = request.files['p_image']
        f_image = request.files['f_image']
        if p_image.filename == '' and f_image.filename == '':
            pass
        if p_image:
            # filename = secure_filename(file.filename)
            ext = p_image.filename
            ext_list = ext.split(".")
            filename = secure_filename(product_name)
            p_image_path = f"images/product_img/{filename}.{ext_list[1]}"

            p_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'] + "/product_img", filename + "." + ext_list[1]))
        if f_image:
            # filename = secure_filename(file.filename)
            ext = f_image.filename
            ext_list = ext.split(".")
            filename = secure_filename(product_name)
            f_image_path = f"images/feature_img/{filename}.{ext_list[1]}"
            p_image.save(os.path.join(
                app.config['UPLOAD_FOLDER'] + "/feature_img", filename + "." + ext_list[1]))

        product = Products.query.filter_by(name=_product_clicked).first()
        product.name = product_name
        product.price = product_price
        product.description = product_description
        
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route("/dashboard/edit_product/<name>",  methods=['GET', 'POST'])
@login_required
def edit_product(name):
    global _product_clicked
    _name = current_user.name
    _email = current_user.email
    _image = current_user.image
    
    _product = Products.query.filter_by(name=name).first()
    _product_clicked = name
    
    return render_template("edit_product.html", _name=_name, _email=_email, _image=_image, p_name=_product.name, p_price=_product.price, p_description=_product.description)


@app.route("/dashboard/delete_product/<name>",  methods=['GET', 'POST'])
@login_required
def delete_product(name):
    Products.query.filter_by(name=name).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/dashboard/coupons")
@login_required
def coupons():

    _name= current_user.name
    _email=current_user.email
    _image=current_user.image
    
    coupon_names = []
    coupon_discount = []
    
    company_coupons = Coupons.query.all()

    print(company_coupons)
    
    for _coupon in company_coupons:
        if _coupon.company == current_user.name:
            coupon_names.append(_coupon.name)
            coupon_discount.append(_coupon.price)
    
    return render_template("coupons.html", _name=_name, _email=_email, _image=_image, coupon_names=coupon_names, coupon_discount=coupon_discount)


@app.route("/dashboard/coupons/create_coupon/",  methods=['GET', 'POST'])
@login_required
def create_coupon():
    _name = current_user.name
    _email = current_user.email
    _image = current_user.image
    
    products=[]
    coupon_products = []
    _products = Products.query.filter_by(company=current_user.name).all()

    for _ in _products:
        products.append(_.name)
    if request.method == "POST":
        coupon_name = request.form['couponName']
        coupon_discount = request.form['discount']
        
        coupon_product = request.form['products']
         
        #id of each product
        coupon_product_id = Products.query.filter_by(name=coupon_product).first()._id
        coupon_products.append(coupon_product_id)
        print(type(coupon_products)) 
        new_coupon = Coupons(name=coupon_name,
                             discount=coupon_discount,
                               company=current_user.name,
                             products=coupon_products)
        db.session.add(new_coupon)
        db.session.commit()
        return redirect(url_for("coupons"))

    return render_template("create_coupon.html", _name=_name, _email=_email, _image=_image, products=products)

@app.route("/contact-us")
def contact():
    return render_template("contact.html")

@app.route("/terms-and-conditions")
def terms_condition():
    return render_template("terms-condition.html")

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True)
