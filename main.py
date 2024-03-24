import re
from model import *
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'QWJhaWt1bWFyIEk='
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route('/home')
def home():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("home.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if session and session['username']:
        return redirect(url_for('home'))
    elif request.method == "GET":
        return render_template("signup.html", msg=None, mail="", pwd="")
    else:
        mail = request.form["mail"]
        pwd = request.form["password"]
    
        if not re.search(r"@gmail\.com$", mail) or len(str(pwd)) < 4:
            return render_template("signup.html", msg="Invalid gmail/password", mail=request.form["mail"], pwd=request.form["password"])
        
        if data.createAccount(request.form["mail"], request.form["password"]):
            return redirect(url_for('login'))
        
        else:
            return render_template("signup.html", msg="Account already exists", mail=request.form["mail"], pwd=request.form["password"])


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session and session['username']:
            return redirect(url_for('home'))
        return render_template("login.html", msg=None, mail="", pwd="")
    else:
        if data.loginAccount(request.form["mail"], request.form["password"]) == True:
            session['username'] = request.form["mail"]
            return redirect(url_for('home'))
        else:
            return render_template("login.html", msg="Invalid User or Password", mail=request.form["mail"], pwd=request.form["password"])


@app.route('/logout')
def logout():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/addItem", methods=["GET"])
def addItem():
    if session and session['username']:
        itemID = request.args.get("itemID")
        if data.addItemToCart(itemID, session["username"]):
            return jsonify({"result": True})
    return jsonify({"result": False})


@app.route('/checkout')
def checkout():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("checkout.html")


@app.route('/getCheckoutList')
def getCheckoutList():
    if session is None or session.get('username') is None:
        return jsonify({"msg": False})
    return jsonify(data.getItemFromCart(session.get('username')))


@app.route('/singlePage')
def singlePage():
    product_id = request.args.get('pid')
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template("product_details.html", pid=product_id)


@app.route('/contact')
def contact():
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('contact.html')


@app.route('/static/<path:filename>')
def static_file(filename):
    return app.send_static_file(filename)


@app.route('/uploads/<path:filename>')
def getImage(filename):
    if session is None or session.get('username') is None:
        return redirect(url_for('login'))
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/get_data', methods=['GET'])
def get_data():
    page = request.args.get("pageno")
    record = data.getData(int(page))
    if record[0]:
        return jsonify({'status': 'success', 'data': record[1]})
    else:
        return jsonify({'status': 'error', 'data': "Error"})


@app.route('/get_single_product', methods=['GET'])
def get_single_product():
    record = data.getSingle(request.args.get("pid"))
    if record[0]:
        return jsonify({'status': 'success', 'data': record[1]})
    else:
        return jsonify({'status': 'error', 'data': "Error"})

@app.route('/setCheckoutData', methods=['POST'])
def setCheckoutData():
    if request.method == "POST":
        record = request.json
        record = record.get('data')
        if data.updateCheckoutData(record, session.get("username")):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error'})
    return jsonify({'status': 'error'})

if __name__ == "__main__":
    app.run(debug=True)
