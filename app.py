from flask import Flask, url_for, request, render_template
import hashlib
from Crypto.Cipher import AES

# Create our flask project
app = Flask(__name__)

# App key and IV
SecretKey = b"A"*16
IV = b"B"*16

def CreateUser(username, password):
    fullcreds = str(username) + "," + hashlib.md5(str(password).encode("ascii")).hexdigest()

    with open("accounts", 'a') as file:
        file.write(fullcreds + "\n")
        file.close()

def AuthUser(username, password):
    password = hashlib.md5(str(password).encode("ascii")).hexdigest()
    fullcred = username+password
    with open("accounts", 'r') as file:
        for user in file.readlines():
            if (fullcred) == user.replace(",", "").strip("\n"):
                return True
        file.close()

def StoreVault(user, data):
    # Create the AES object
    obj = AES.new(SecretKey, AES.MODE_CFB, IV=IV)
    
    # Convert the data to bytes
    plain_vault = bytes(data)

    # Encrypt the vault
    encrypted_vault = obj.encrypt(plain_vault)

    # Store the vault
    file = open("vaults/"+user+".vault", "wb")
    file.write(encrypted_vault)
    file.close()

def RetVault(user):
    # Create the AES object
    obj = AES.new(SecretKey, AES.MODE_CFB, IV=IV)
    
    # Retrieve the user's vault
    file = open("vaults/"+user+".vault", "rb")

    # Decrypt the vault
    decrypted_vault = obj.decrypt(file.read())
    file.close()

    # Send the vault back
    return(decrypted_vault.decode("utf-8"))

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register",methods=['POST'])
def register():
    # Assign user and pass vars
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    # Create the user
    CreateUser(username, password)

    return "User created!"

@app.route("/importvault",methods=['POST'])
def importvault():
    # Assign user and pass vars
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        vault = request.files['vault']

    # Authenticate the user
    if AuthUser(username, password):
        StoreVault(username, vault.read())
        return "Vault has been uploaded!"
    else:
        return "Incorrect Creds"

@app.route("/getvault",methods=['POST'])
def getvault():
    # Assign user and pass vars
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    # Authenticate the user
    if AuthUser(username, password):
        return ("Here is your vault: \n"+RetVault(username))
    else:
        return "Incorrect Creds"

if __name__== '__main__':
    app.run(host='0.0.0.0', port=8080)
