from flask import Flask, render_template, request
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

app = Flask(__name__)

backend_url = "http://127.0.0.1:5000"
response = requests.get(f"{backend_url}/get_public_key")

# Fetch Public Key On Boot
backend_public_key = RSA.import_key(response.json()["public_key"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        user_input = request.form["user_input"]
        # RSA-Encrypt user input with backend's public RSA key
        cipher_rsa = PKCS1_OAEP.new(backend_public_key)
        encrypted_text = cipher_rsa.encrypt(user_input.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted_text).decode("utf-8")
        # Send RSA-encrypted text to backend
        response = requests.post(
            f"{backend_url}/process_text", json={"encrypted_text": encrypted_b64}
        )
        # Display Quantum-Safe Encrypted Text
        pq_encrypted_text = response.json()["pq_encrypted_text"]
        return render_template("index.html", result=pq_encrypted_text)
    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
