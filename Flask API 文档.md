## Flask API 文档

### 1. 首页

**Endpoint**: `/`

**Method**: `GET`

**Description**: 返回首页的HTML内容。

---

### 2. 加密（简单模式）

**Endpoint**: `/api/encrypt`

**Method**: `POST`

**Body**:

```json
{
    "plaintext": "<十六进制格式的明文>",
    "key": "<十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "ciphertext": "<十六进制格式的密文>"
}
```

**Description**: 使用给定的密钥加密十六进制格式的明文。

---

### 3. 解密（简单模式）

**Endpoint**: `/api/decrypt`

**Method**: `POST`

**Body**:

```json
{
    "ciphertext": "<十六进制格式的密文>",
    "key": "<十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "plaintext": "<十六进制格式的明文>"
}
```

**Description**: 使用给定的密钥解密十六进制格式的密文。

---

### 4. 字符串加密

**Endpoint**: `/api/encrypt_string`

**Method**: `POST`

**Body**:

```json
{
    "input_str": "<待加密的字符串>",
    "key": "<十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "encrypted_base64_str": "<Base64编码的加密结果>"
}
```

**Description**: 使用给定的密钥加密字符串，并返回Base64编码的加密结果。

---

### 5. 字符串解密

**Endpoint**: `/api/decrypt_string`

**Method**: `POST`

**Body**:

```json
{
    "encrypted_base64_str": "<Base64编码的加密字符串>",
    "key": "<十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "output_str": "<解密后的字符串>"
}
```

**Description**: 使用给定的密钥解密Base64编码的加密字符串。

---

### 6. 双密钥加密

**Endpoint**: `/api/double_encrypt`

**Method**: `POST`

**Body**:

```json
{
    "plaintext": "<十六进制格式的明文>",
    "key": "<连续的两个十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "double_ciphertext": "<十六进制格式的双密文>"
}
```

**Description**: 使用两个密钥进行加密操作。

---

### 7. 双密钥解密

**Endpoint**: `/api/double_decrypt`

**Method**: `POST`

**Body**:

```json
{
    "ciphertext": "<十六进制格式的双密文>",
    "key": "<连续的两个十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "double_plaintext": "<十六进制格式的双明文>"
}
```

**Description**: 使用两个密钥进行解密操作。

---

### 8. 三重加密

**Endpoint**: `/api/tri_encrypt`

**Method**: `POST`

**Body**:

```json
{
    "plaintext": "<十六进制格式的明文>",
    "key": "<连续的三个十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "tri_ciphertext": "<十六进制格式的三重密文>"
}
```

**Description**: 使用三个密钥进行加密操作。

---

### 9. 三重解密

**Endpoint**: `/api/tri_decrypt`

**Method**: `POST`

**Body**:

```json
{
    "ciphertext": "<十六进制格式的三重密文>",
    "key": "<连续的三个十六进制格式的密钥>"
}
```

**Response**:

```json
{
    "tri_plaintext": "<十六进制格式的三重明文>"
}
```

**Description**: 使用三个密钥进行解密操作。

---

### 10. 破解密钥

**Endpoint**: `/api/crack`

**Method**: `POST`

**Body**:

```json
{
    "pairs": [
        {
            "plaintext": "<十六进制格式的明文>",
            "ciphertext": "<十六进制格式的密文>"
        },
        ...
    ]
}
```

**Response**:

```json
{
    "result": {
        "keys": [
            {
                "key1": "<第一个密钥>",
                "key2": "<第二个密钥>"
            },
            ...
        ],
        "timeTaken": <操作所用的时间（秒）>
    },
    "status": "<状态：'success'或'failure'>",
    "message": "<相关消息>"
}
```

**Description**: 通过提供的明密文对尝试破解密钥。

---

### 11. CBC模式加密

**Endpoint**: `/api/cbc/encrypt`

**Method**: `POST`

**Body**:

```json
{
    "longtext": "<十六进制格式的长明文>",
    "key": "<十六进制格式的密钥>",
    "IV": "<十六进制格式的初始化向量>"
}
```

**Response**:

```json
{
    "encrypted": "<十六进制格式的加密结果>"
}
```

**Description**: 使用CBC模式和给定的密钥、初始化向量进行加密。

---

### 12. CBC模式解密

**Endpoint**: `/api/cbc/decrypt`

**Method**: `POST`

**Body**:

```json
{
    "longcipher": "<十六进制格式的长密文>",
    "key": "<十六进制格式的密钥>",
    "IV": "<十六进制格式的初始化向量>"
}
```

**Response**:

```json
{
    "decrypted": "<十六进制格式的解密结果>"
}
```

**Description**: 使用CBC模式和给定的密钥、初始化向量进行解密。



