from flask import Flask, make_response, jsonify, Response, request
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {"Login": "Login"}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = 'commander09'
app.config['MYSQL_DB'] = 'restoreservation'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return "<p>This is my list!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

@app.route("/tblcustomers", methods=["GET"])
@auth.login_required
def get_tblcustomers():
    data = data_fetch("""SELECT * FROM tblcustomers""")
    return make_response(jsonify(data), 200)


@app.route("/tblcustomers/<int:id>", methods=["GET"])
@auth.login_required
def get_tblcustomers_by_id(id):
    data = data_fetch("""SELECT * FROM tblcustomers WHERE customer.id = {}""".format(id))
    myResponse = make_response(jsonify(data))
    return myResponse


@app.route("/tblcustomers", methods=['POST'])
@auth.login_required
def add_tblcustomers():
    cur = mysql.connection.cursor()
    json = request.get_json(force=True)
    firstname = json["firstname"]
    lastname = json["lastname"]
    phone_number = json["phone_number"]
    cur.execute(
        """ INSERT INTO tblcustomers (firstname, lastname, phone_number) VALUE (%s, %s, %s)""", (firstname, lastname, phone_number),
    )
    mysql.connection.commit()
    _response = jsonify("customer is added successfully!")
    _response.status_code = 200
    cur.close()
    return _response

@app.route("/tblcustomers/<int:id>", methods=["PUT"])
@auth.login_required
def update_customer_by_id(id):
    cur = mysql.connection.cursor()
    json = request.get_json(force=True)
    firstname = json["firstname"]
    lastname = json["lastname"]
    phone_number = json["phone_number"]
    cur.execute(""" UPDATE tblcustomers SET firstname = %s, lastname = %s, phone_number = %s WHERE customer_id = %s""", (firstname, lastname, phone_number, id))
    mysql.connection.commit()
    _response = jsonify("Customer is updated successfully!")
    _response.status_code = 200
    cur.close()
    return _response





@app.route("/tblcustomers/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_customer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM tblcustomers WHERE customer_id = %s""", (id,))
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "Customer deleted successfully"}), 200)



@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        

if __name__ == "__main__":
    app.run()
    app.run(debug=True)