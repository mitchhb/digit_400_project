from flask import Flask, render_template, url_for, flash, request, redirect, session, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from pymysql import escape_string as thwart
from functools import wraps
from datetime import datetime, timedelta
import gc
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from content import Content
from db_connect import connection

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login.")
            return redirect(url_for('login'))

APP_CONTENT = Content()

APP_CONTENT = {
    "Home":[["Chassis Mount Wing", "/chassismountwing/","Check out the popular Chassis Mount Wings for many different cars!", "https://cdn.shopify.com/s/files/1/0919/7894/products/28513873682_3fe6bc8374_o_grande.jpg?v=1512449671"]],
    "Profile":[["User Profile", "/profile/", "Edit your profile here!", "https://cdn.wallpapersafari.com/11/79/xMyfJT.jpg"],
              ["Settings", "/settings/", "App Settins, no biggie."],
              ["Terms of Sercive", "/tos/", "The legal stuff."],],
    "Messages":[["Messsages", "/messages/", "Your user messages are waiting...", "https://cdn.wallpapersafari.com/11/79/xMyfJT.jpg"],
               ["Alerts", "/alerts/", "!!Urgent Alerts!!"],],
    "Contact":[["Contact", "/contact/", "Contact us for support.", "https://cdn.wallpapersafari.com/11/79/xMyfJT.jpg"],],
}


@app.route("/")
def index():
    error = ""
    
    try:
        c, conn = connection()
        if request.method == "POST":
            
            data = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(request.form['username'])))
            
            data = c.fetchone()[2]
            
            if sha256_crypt.verify(request.form["password"], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                
                flash("You are now logged in"+session['username']+"!")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid Credentials, try again!"
                
        return render_template("main.html", error = error)
    
    except Exception as e:
        return render_template("main.html", error = error)
    

@app.route("/dashboard/")
def dashboard():
    try:
        return render_template("dashboard.html", APP_CONTENT = APP_CONTENT)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route("/login/", methods=["GET", "POST"])
def login():
    error = ""
    
    try:
        c, conn = connection()
        if request.method == "POST":
            
            data = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(request.form['username'])))
            
            data = c.fetchone()[2]
            
            if sha256_crypt.verify(request.form["password"], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                
                flash("You are now logged in"+session['username']+"!")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid Credentials, try again!"
                
        return render_template("login.html", error = error)
    
    except Exception as e:
        flash(e) # remove for production
        error = "Invalid Credentials, try again!"
        return render_template("login.html", error = error)
    
@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for("index"))

class RegistrationForm(Form):
    username = TextField("Username", [validators.length(min=4, max=20)])
    email = TextField("Email Address", [validators.length(min=6, max=50)])
    password = PasswordField("New Password", [validators.Required(),
                                             validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField("I accept the Terms of Service and Privacy Notice", [validators.Required()])

@app.route('/register/', methods=["GET", "POST"])
def register():
    
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            
            c, conn = connection() #if it runs, it will post a string
            return("Connected")
            
            x = c.execute("SELECT * FROM users WHERE username = ('{0}')", format((thwart(username))))
            
            if int(x) > 0:
                flash("That username is already taken, please choose another.")
                return render_template("register.html", form = form)
            else:
                c.execute("INSERT INTO users (username,password,email,tracking) VALUES ('{0}'), ('{1}'), ('{2}'), ('{3}')".format(thwart(username), thwart(password), thwart(email), thwart("/dashboard/")))
                
                conn.commit()
                flash("Thanks for registering, "+username+"!")
                conn.close()
                gc.collect()
                
                session['logged_in'] = True
                session['username'] = username
                
                return redirect(url_for('dashboard'))
        return render_template("register.html", form = form)
            
        
    except Exception as e:
            return(str(e)) # remember to remove! for debugging only!
        
@app.route('/about/')
def about():
    try:
        return render_template("about.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/companies/')
def companies():
    try:
        return render_template("companies.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/support/')
def support():
    try:
        return render_template("support.html")
    except Exception as e:
        return render_template("500.html", error = e)   

        
@app.route('/chassismountwing/')
def chassis():
    try:
        return render_template("chassismountwing.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/duckbillwing/')
def duckbill():
    try:
        return render_template("duckbillwing.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/trunkmounted/')
def trunkmount():
    try:
        return render_template("trunkmountwing.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/nissan/')
def chassis350z():
    try:
        return render_template("chassisnissan.html",)
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/duckbillwing/nissan/')
def duckbillnissan():
    try:
        return render_template("duckbillnissan.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/subaru/')
def chassissubaru():
    try:
        return render_template("chassissubaru.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/duckbillwing/subaru/')
def duckbillsubaru():
    try:
        return render_template("duckbillsubaru.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/duckbillwing/mitsubishi/')
def duckbillmitsubishi():
    try:
        return render_template("duckbillmitsubishi.html",)
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/duckbillwing/infiniti/')
def duckbillinfinti():
    try:
        return render_template("duckbillinfinti.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/duckbillwing/hyundai/')
def duckbillhyundai():
    try:
        return render_template("duckbillhyundai.html",)
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/duckbillwing/honda/')
def duckbillhonda():
    try:
        return render_template("duckbillhonda.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/duckbillwing/scion/')
def duckbillscion():
    try:
        return render_template("duckbillscion.html",)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/bmw/')
def bmw():
    try:
        return render_template("chassisbmw.html")
    except Exception as e:
        return render_template("500.html", error = e)   
    
@app.route('/chassismountwing/chevrolet/')
def chevy():
    try:
        return render_template("chassischevy.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/dodge/')
def dodge():
    try:
        return render_template("chassisdodge.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/ford/')
def ford():
    try:
        return render_template("chassisford.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/honda/')
def honda():
    try:
        return render_template("chassishonda.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/chassismountwing/hyundai/')
def hyundai():
    try:
        return render_template("chassishyundai.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/infiniti/')
def infiniti():
    try:
        return render_template("chassisinfiniti.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/chassismountwing/lexus/')
def lexus():
    try:
        return render_template("chassislexus.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/chassismountwing/mazda/')
def mazda():
    try:
        return render_template("chassismazda.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/scion/')
def scion():
    try:
        return render_template("chassisscion.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/chassismountwing/toyota/')
def toyota():
    try:
        return render_template("chassistoyota.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/trunkmountwing/nissan/')
def trunknissan():
    try:
        return render_template("trunknissan.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/trunkmountwing/subaru/')
def trunksubaru():
    try:
        return render_template("trunksubaru.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/trunkmountwing/mitsubishi/')
def trunkmitsu():
    try:
        return render_template("trunkmitsubishi.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/trunkmountwing/mazda/')
def trunkmazda():
    try:
        return render_template("trunkmazda.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/trunkmountwing/scion/')
def trunkscion():
    try:
        return render_template("trunkscion.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/trunkmountwing/toyota/')
def trunktoyota():
    try:
        return render_template("trunktoyota.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/bodykits/')
def bodykits():
    try:
        return render_template("bodykits.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/diffusers/')
def diffusers():
    try:
        return render_template("diffusers.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/splitters/')
def splitters():
    try:
        return render_template("splitters.html")
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/decals/')
def decals():
    try:
        return render_template("decals.html")
    except Exception as e:
        return render_template("500.html", error = e)
    
    
@app.route('/welcome/')
def welcome():
    try:
        return render_template("welcome.html")
    except Exception as e:
        return render_template("500.html", error = e) 

        
#sitemap

@app.route('/sitemap.xml/', methods=["GET"])
def sitemap():
    try:
        pages = []
        week = (datetime.now() - timedelta(days = 7)).date().isoformat()
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments) == 0:
                pages.append(["http://104.248.126.178"+str(rule.rule), week])
        sitemap_xml = render_template('sitemap_template.xml', pages = pages)
        response = make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"
        return response
    
    except Exception as e:
        return(str(e))
    
@app.route("/robots.txt")
def robots():
    return("User-agent: \nDisallow: /login \nDisallow: /register")

## Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("405.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", error = e)


if __name__ == "__main__":
    app.run(debug=True) #This should be turned off?False for production.