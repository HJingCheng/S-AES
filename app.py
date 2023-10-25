import time

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from SAES import SAES

app = Flask(__name__)
app.secret_key = "123456789"

saes = SAES()  # 创建SAES对象


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    data = request.json
    plaintext = data['plaintext']
    key = data['key']
    # 将普通字符串转换为十六进制
    plaintext_int = int(plaintext, 16)
    key_int = int(key, 16)
    result = saes.encrypt(plaintext_int, key_int)
    result = hex(result)
    return jsonify({"ciphertext": result})


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key = data['key']
    ciphertext_int = int(ciphertext, 16)
    key_int = int(key, 16)
    result = saes.decrypt(ciphertext_int, key_int)
    result = hex(result)
    return jsonify({"plaintext": result})


@app.route('/api/encrypt_string', methods=['POST'])
def api_encrypt_string():
    data = request.json
    input_str = data['input_str']
    key = data['key']
    key_int = int(key, 16)
    result = saes.encrypt_string(input_str, key_int)
    return jsonify({"encrypted_base64_str": result})


@app.route('/api/decrypt_string', methods=['POST'])
def api_decrypt_string():
    data = request.json
    encrypted_base64_str = data['encrypted_base64_str']
    key = data['key']
    key_int = int(key, 16)
    result = saes.decrypt_string(encrypted_base64_str, key_int)
    return jsonify({"output_str": result})


@app.route('/api/double_encrypt', methods=['POST'])
def api_double_encrypt():
    data = request.json
    plaintext = data['plaintext']
    key = data['key']
    plaintext_int = int(plaintext, 16)
    # 将key划分为key1和key2
    key1 = key[0:4]
    key2 = key[4:8]
    key_int = int(key1, 16)
    key2_int = int(key2, 16)
    result = saes.double_encrypt(plaintext_int, key_int, key2_int)
    result = hex(result)
    return jsonify({"double_ciphertext": result})


@app.route('/api/double_decrypt', methods=['POST'])
def api_double_decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key = data['key']
    ciphertext_int = int(ciphertext, 16)
    # 将key划分为key1,key2
    key1 = key[0:4]
    key2 = key[4:8]
    key1_int = int(key1, 16)
    key2_int = int(key2, 16)
    result = saes.double_decrypt(ciphertext_int, key1_int, key2_int)
    result = hex(result)
    return jsonify({"double_plaintext": result})


@app.route('/api/tri_encrypt', methods=['POST'])
def api_tri_encrypt():
    data = request.json
    plaintext = data['plaintext']
    key = data['key']
    # 将key划分为key1,key2,key3
    key1 = key[0:4]
    key2 = key[4:8]
    key3 = key[8:12]
    plaintext_int = int(plaintext, 16)
    key1_int = int(key1, 16)
    key2_int = int(key2, 16)
    key3_int = int(key3, 16)
    result = saes.tri_encrypt(plaintext_int, key1_int, key2_int, key3_int)
    result = hex(result)
    return jsonify({"tri_ciphertext": result})


@app.route('/api/tri_decrypt', methods=['POST'])
def api_tri_decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key = data['key']
    # 将key划分为key1,key2,key3
    key1 = key[0:4]
    key2 = key[4:8]
    key3 = key[8:12]
    ciphertext_int = int(ciphertext, 16)
    key1_int = int(key1, 16)
    key2_int = int(key2, 16)
    key3_int = int(key3, 16)
    result = saes.tri_decrypt(ciphertext_int, key1_int, key2_int, key3_int)
    result = hex(result)
    return jsonify({"tri_plaintext": result})


@app.route('/api/crack', methods=['POST'])
def crack():
    data = request.json
    pairs = data['pairs']

    # 转换数据类型
    formatted_pairs = []
    for pair in pairs:
        plaintext = int(pair['plaintext'], 16)  # 将十六进制字符串转换为整数
        ciphertext = int(pair['ciphertext'], 16)
        formatted_pairs.append({'plaintext': plaintext, 'ciphertext': ciphertext})

    start_time = time.time()
    key_pairs_found = saes.MitMAttack(formatted_pairs)
    end_time = time.time()
    time_spent = end_time - start_time

    keys_found_str = []
    if key_pairs_found:
        for key_pair in key_pairs_found:
            key1_str = hex(key_pair[0])[2:]  # 转为十六进制并移除'0x'前缀
            key2_str = hex(key_pair[1])[2:]
            keys_found_str.append({"key1": key1_str, "key2": key2_str})
    else:
        keys_found_str.append("No keys found that match all pairs")

    response_data = {
        "result": {
            "keys": keys_found_str,
            "timeTaken": time_spent
        },
        "status": "success" if key_pairs_found else "failure",
        "message": "Operation completed successfully" if key_pairs_found else "No matching keys found"
    }

    return jsonify(response_data)


@app.route('/api/cbc/encrypt', methods=['POST'])
def api_cbc_encrypt():
    data = request.json
    longtext = int(data['longtext'], 16)
    key = int(data['key'], 16)
    IV = int(data['IV'], 16)
    print(hex(longtext), hex(key), hex(IV))
    encrypted = saes.CBC_encrypt(longtext, key, IV)
    return jsonify({
        "encrypted": hex(encrypted)
    })


@app.route('/api/cbc/decrypt', methods=['POST'])
def api_cbc_decrypt():
    data = request.json
    longcipher = int(data['longcipher'], 16)
    key = int(data['key'], 16)
    IV = int(data['IV'], 16)

    decrypted = saes.CBC_decrypt(longcipher, key, IV)
    return jsonify({
        "decrypted": hex(decrypted)
    })


if __name__ == '__main__':
    app.run()
