from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from base64 import b64encode
import urllib.parse

app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Lấy thông tin từ request JSON
    encoded_key = request.json['key']
    password = request.json['password']
    hash_value = request.json['hash_value']

    # Giải mã URL encoded key
    decoded_key = urllib.parse.unquote(encoded_key)

    # Chuyển đổi khóa công khai từ chuỗi
    public_key_bytes = decoded_key.encode()
    public_key = serialization.load_pem_public_key(public_key_bytes)

    # Mã hóa dữ liệu
    cipher_text = public_key.encrypt(
        (hash_value + password).encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

    # Chuyển đổi dữ liệu đã mã hóa sang dạng base64
    encoded_cipher_text = b64encode(cipher_text).decode()

    # Trả lại dữ liệu đã mã hóa
    return jsonify({'encrypted_data': encoded_cipher_text})

if __name__ == '__main__':
    app.run(debug=True)
