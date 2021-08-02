from flask import Flask, request, jsonify
import modules.extract_features_controller as EFC
import json
from flask_mysqldb import MySQL
import jwt
import modules.config as cfg

app = Flask(__name__)

app.config['MYSQL_HOST'] = cfg.HOST
app.config['MYSQL_USER'] = cfg.USER
app.config['MYSQL_PASSWORD'] = cfg.PASSWORD
app.config['MYSQL_DB'] = cfg.DATABASE
app.config['SECRET'] = cfg.SECRET

mysql = MySQL(app)



@app.route("/", methods=["GET"])
def home_page():
    return "THIS IS API"
    


@app.route("/api/extract_features", methods=["POST"])
def extract_features_handler():
    token = request.headers["Authorization"].split(' ')[1]
    payload = jwt.decode(token, app.config['SECRET'], algorithms=["HS256"])
    receivedApiKey = request.form["apiKey"]
    username = payload['username']
    cur = mysql.connection.cursor()
    cur.execute(f"CALL GetApiKey('{username}')")
    userApiKey = cur.fetchall()[0][0]
    cur.close()
    if(receivedApiKey == userApiKey):
        f = request.files['file']
        matched_face_ids = EFC.extract_features(f)
    return json.dumps(matched_face_ids)


if __name__ == '__main__':
    app.run(debug=True)