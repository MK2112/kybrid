from flask import Flask, request, jsonify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt as pq_decrypt
import base64

app = Flask(__name__)

# RSA Key Generation
rsa_key = RSA.generate(2048)
private_key = rsa_key.export_key()
public_key = rsa_key.publickey().export_key()

# Post-Quantum Key Pair Generation
pq_public_key, pq_private_key = generate_keypair()


@app.route("/get_public_key", methods=["GET"])
def get_public_key():
    return jsonify({"public_key": public_key.decode("utf-8")})


@app.route("/process_text", methods=["POST"])
def process_text():
    try:
        encrypted_text = request.json["encrypted_text"]
        encrypted_bytes = base64.b64decode(encrypted_text)
        rsa_cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_text = rsa_cipher.decrypt(encrypted_bytes).decode("utf-8")
        ciphertext, shared_secret = encrypt(
            pq_public_key, decrypted_text.encode("utf-8")
        )
        return jsonify(
            {"pq_encrypted_text": base64.b64encode(ciphertext).decode("utf-8")}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
