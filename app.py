from flask import Flask, url_for, request
import hashlib
from Crypto.Cipher import AES

# Create our flask project
app = Flask(__name__)

ServerKey = 'This is a key123'.encode('utf-8')

@app.route("/")
def hello():
    return "Hello there!"

@app.route("/register",methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        fullcreds = str(username) + "," + hashlib.md5(str(password).encode("ascii")).hexdigest()

    with open("accounts", 'a') as file:
        file.write(fullcreds + "\n")
        file.close()
    
    return fullcreds

@app.route("/importvault/<username>/<password>",methods=['POST'])
def importvault(username, password):
    password = hashlib.md5(str(password).encode("ascii")).hexdigest()
    fullcred = username+password

    with open("accounts", 'r') as file:
        for user in file.readlines():
            if (fullcred) == user.replace(",", "").strip("\n"):
                if request.method == 'POST':
                    f = request.files['file']
                    f.save(fullcred)

                with open(fullcred, "r") as vault:
                    vault.readlines()
                    vault.close()

                return "Your vault has been uploaded"
            else:
                return "Bad"

        file.close()
