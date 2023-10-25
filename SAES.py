import base64


class SAES:
    def __init__(self):
        self.SBox = [
            [0x9, 0x4, 0xA, 0xB],
            [0xD, 0x1, 0x8, 0x5],
            [0x6, 0x2, 0x0, 0x3],
            [0xC, 0xE, 0xF, 0x7]
        ]

        self.InvSBox = [
            [0xA, 0x5, 0x9, 0xB],
            [0x1, 0x7, 0x8, 0xF],
            [0x6, 0x0, 0x2, 0x3],
            [0xC, 0x4, 0xD, 0xE]
        ]

        self.Rcon = [0x80, 0x30]

    def sub_nibbles(self, word, inv=False):
        sbox = self.InvSBox if inv else self.SBox
        new_word = 0
        for i in range(0, 16, 4):
            nibble = (word >> i) & 0xF  # 提取4位
            row = (nibble >> 2) & 0x3
            col = nibble & 0x3
            subbed_nibble = sbox[row][col]
            new_word |= (subbed_nibble << i)  # 插入新的4位

        return new_word

    def shift_rows(self, word):
        # 提取各个字节
        byte1 = (word & 0xF000) >> 12
        byte2 = (word & 0x0F00) >> 8
        byte3 = (word & 0x00F0) >> 4
        byte4 = word & 0x000F

        # 根据描述，我们应该交换byte2和byte4
        result = (byte1 << 12) | (byte4 << 8) | (byte3 << 4) | byte2

        return result

    def gf_mult(self, a, b, mod_polynomial):
        # Polynomial multiplication in GF(2^4) without reduction
        p = 0
        while b:
            if b & 1:
                p ^= a
            a <<= 1
            b >>= 1
        return p

    def gf_mod(self, p, mod_polynomial):
        # Polynomial modulo operation in GF(2^4)
        # Get the degree of mod_polynomial
        degree_mod = 0
        temp_mod = mod_polynomial
        while temp_mod:
            temp_mod >>= 1
            degree_mod += 1

        # Reduce p using mod_polynomial
        degree_p = 0
        temp_p = p
        while temp_p:
            temp_p >>= 1
            degree_p += 1

        while degree_p >= degree_mod:
            p ^= mod_polynomial << (degree_p - degree_mod)
            temp_p = p
            degree_p = 0
            while temp_p:
                temp_p >>= 1
                degree_p += 1

        return p

    def gf_multiply(self, a, b, mod_polynomial):
        return self.gf_mod(self.gf_mult(a, b, mod_polynomial), mod_polynomial)

    def mix_columns(self, word):
        mod_polynomial = 0b10011  # This represents x^4 + x + 1

        # Extract the matrix values from the word
        val11 = (word & 0xF000) >> 12
        val12 = (word & 0x0F00) >> 8
        val21 = (word & 0x00F0) >> 4
        val22 = word & 0x000F

        # Multiply the values by the matrix
        res11 = self.gf_multiply(val11, 1, mod_polynomial) ^ self.gf_multiply(val12, 4, mod_polynomial)
        res12 = self.gf_multiply(val11, 4, mod_polynomial) ^ self.gf_multiply(val12, 1, mod_polynomial)
        res21 = self.gf_multiply(val21, 1, mod_polynomial) ^ self.gf_multiply(val22, 4, mod_polynomial)
        res22 = self.gf_multiply(val21, 4, mod_polynomial) ^ self.gf_multiply(val22, 1, mod_polynomial)

        # Construct the result word
        result = (res11 << 12) | (res12 << 8) | (res21 << 4) | res22
        return result

    def inv_mix_columns(self, word):
        mod_polynomial = 0b10011  # This represents x^4 + x + 1

        # Extract the matrix values from the word
        val11 = (word & 0xF000) >> 12
        val12 = (word & 0x0F00) >> 8
        val21 = (word & 0x00F0) >> 4
        val22 = word & 0x000F

        # Multiply the values by the inverse matrix
        res11 = self.gf_multiply(val11, 9, mod_polynomial) ^ self.gf_multiply(val12, 2, mod_polynomial)
        res12 = self.gf_multiply(val11, 2, mod_polynomial) ^ self.gf_multiply(val12, 9, mod_polynomial)
        res21 = self.gf_multiply(val21, 9, mod_polynomial) ^ self.gf_multiply(val22, 2, mod_polynomial)
        res22 = self.gf_multiply(val21, 2, mod_polynomial) ^ self.gf_multiply(val22, 9, mod_polynomial)

        # Construct the result word
        result = (res11 << 12) | (res12 << 8) | (res21 << 4) | res22
        return result

    def g_function(self, byte, round_number):
        # Rotate the 8-bit byte 4 bits to the left
        rotated = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)

        # Substitute the byte
        substituted = self.sub_byte(rotated)

        # XOR with the round constant
        return substituted ^ self.Rcon[round_number]

    def sub_byte(self, byte, inv=False):
        """This function performs substitution on an 8-bit byte."""
        sbox = self.InvSBox if inv else self.SBox
        # Extract the two 4-bit nibbles
        high_nibble = (byte & 0xF0) >> 4
        low_nibble = byte & 0x0F

        # Substitute each nibble
        row_high = (high_nibble >> 2) & 0x3
        col_high = high_nibble & 0x3
        row_low = (low_nibble >> 2) & 0x3
        col_low = low_nibble & 0x3

        subbed_high_nibble = sbox[row_high][col_high]
        subbed_low_nibble = sbox[row_low][col_low]

        # Combine the substituted nibbles back into a byte
        return (subbed_high_nibble << 4) | subbed_low_nibble

    def key_expansion(self, key):
        w = [0] * 6  # Array to store w0 to w5

        # Initialize w0 and w1
        w[0] = (key & 0xFF00) >> 8
        w[1] = key & 0x00FF

        # Calculate w2 and w3
        w[2] = w[0] ^ self.g_function(w[1], 0)
        w[3] = w[2] ^ w[1]

        # Calculate w4 and w5
        w[4] = w[2] ^ self.g_function(w[3], 1)
        w[5] = w[4] ^ w[3]
        return w

    def encrypt(self, plaintext, key):
        # Key expansion
        w = self.key_expansion(key)

        # Initial round key addition
        ciphertext = plaintext ^ (w[0] << 8 | w[1])
        # --- Round 1 ---
        # SubNibbles
        ciphertext = self.sub_nibbles(ciphertext)
        # ShiftRows
        ciphertext = self.shift_rows(ciphertext)
        # MixColumns
        ciphertext = self.mix_columns(ciphertext)
        # AddRoundKey with w2 and w3
        ciphertext = ciphertext ^ (w[2] << 8 | w[3])

        # --- Round 2 ---
        # SubNibbles
        ciphertext = self.sub_nibbles(ciphertext)
        # ShiftRows
        ciphertext = self.shift_rows(ciphertext)
        # AddRoundKey with w4 and w5
        ciphertext = ciphertext ^ (w[4] << 8 | w[5])

        return ciphertext

    def decrypt(self, ciphertext, key):
        # Key expansion
        w = self.key_expansion(key)

        # Initial round key subtraction (using w4 and w5)
        plaintext = ciphertext ^ (w[4] << 8 | w[5])

        # --- Inverse of Round 2 ---
        # InvShiftRows
        plaintext = self.shift_rows(plaintext)
        # InvSubNibbles
        plaintext = self.sub_nibbles(plaintext, inv=True)
        # AddRoundKey (using w2 and w3)
        plaintext = plaintext ^ (w[2] << 8 | w[3])

        # --- Inverse of Round 1 ---
        # InvMixColumns
        plaintext = self.inv_mix_columns(plaintext)  # MixColumns is its own inverse
        # InvShiftRows
        plaintext = self.shift_rows(plaintext)
        # InvSubNibbles
        plaintext = self.sub_nibbles(plaintext, inv=True)
        # AddRoundKey (using w0 and w1)
        plaintext = plaintext ^ (w[0] << 8 | w[1])

        return plaintext

    def encrypt_string(self, input_str, key):
        # Convert string to ASCII values
        ascii_values = [ord(c) for c in input_str]

        # Check for padding
        if len(ascii_values) % 2 != 0:
            ascii_values.append(0x00)  # Add padding

        encrypted_values = []

        for i in range(0, len(ascii_values), 2):
            # Convert two bytes to 16-bit word
            word = (ascii_values[i] << 8) | ascii_values[i + 1]

            # Encrypt the word
            encrypted_word = self.encrypt(word, key)

            # Append encrypted bytes to the list
            encrypted_values.append((encrypted_word & 0xFF00) >> 8)
            encrypted_values.append(encrypted_word & 0x00FF)

        # Convert encrypted values to a byte array
        encrypted_byte_array = bytearray(encrypted_values)

        # Encode the byte array to Base64
        encrypted_base64_str = base64.b64encode(encrypted_byte_array).decode('utf-8')

        return encrypted_base64_str

    def decrypt_string(self, encrypted_base64_str, key):
        # Decode the Base64 string to a byte array
        encrypted_byte_array = base64.b64decode(encrypted_base64_str)

        # Convert the byte array to a list of ASCII values
        ascii_values = list(encrypted_byte_array)

        # Ensure the encrypted data is valid
        if len(ascii_values) % 2 != 0:
            raise ValueError("Invalid encrypted data")

        decrypted_values = []

        for i in range(0, len(ascii_values), 2):
            # Convert two bytes to 16-bit word
            word = (ascii_values[i] << 8) | ascii_values[i + 1]

            # Decrypt the word
            decrypted_word = self.decrypt(word, key)

            # Append decrypted bytes to the list
            decrypted_values.append((decrypted_word & 0xFF00) >> 8)
            decrypted_values.append(decrypted_word & 0x00FF)

        # Remove padding if present
        if decrypted_values[-1] == 0x00:
            decrypted_values = decrypted_values[:-1]

        # Convert decrypted values back to ASCII string
        decrypted_str = ''.join([chr(val) for val in decrypted_values])

        return decrypted_str

    # 双重加密函数
    # key为8位十六进制数，总长32bit
    def double_encrypt(self, plaintext, key1, key2):
        mid_text = self.encrypt(plaintext, key1)
        double_encrypted_text = self.encrypt(mid_text, key2)  # 使用key2进行加密
        return double_encrypted_text

    # 双重解密函数
    def double_decrypt(self, ciphertext, key1, key2):
        mid_text = self.decrypt(ciphertext, key2)  # 使用key2进行解密
        double_decrypted_text = self.decrypt(mid_text, key1)
        return double_decrypted_text

    # 三重加密
    def tri_encrypt(self, plaintext, key1, key2, key3):
        mid_text = self.encrypt(plaintext, key1)
        mid_text = self.encrypt(mid_text, key2)
        cipher_text = self.encrypt(mid_text, key3)
        return cipher_text

    def tri_decrypt(self, ciphertext, key1, key2, key3):
        mid_text = self.decrypt(ciphertext, key3)
        mid_text = self.decrypt(mid_text, key2)
        plain_text = self.decrypt(mid_text, key1)
        return plain_text

    # 中间相遇攻击
    # def MitMAttack(self, plaintext, ciphertext):
    #     for k1 in range(0xffff):
    #         for k2 in range(0xffff):
    #             if self.encrypt(plaintext, k1) == self.encrypt(ciphertext, k2):
    #                 return k1 * 65536 + k2
    def MitMAttack(self, pairs):
        # 这个字典用于存储每个明文通过k1加密后的结果
        encrypt_dicts = [{} for _ in pairs]

        # 为每个明密文对和每个可能的k1加密明文
        for index, pair in enumerate(pairs):
            plaintext = pair['plaintext']
            for k1 in range(0xffff):
                encrypted = self.encrypt(plaintext, k1)
                if encrypted not in encrypt_dicts[index]:
                    encrypt_dicts[index][encrypted] = []
                encrypt_dicts[index][encrypted].append(k1)

        # 这个字典用于统计每个k1,k2组合的出现次数
        key_pair_counts = {}

        # 对于所有可能的k2，解密密文
        for k2 in range(0xffff):
            for index, pair in enumerate(pairs):
                ciphertext = pair['ciphertext']
                decrypted = self.decrypt(ciphertext, k2)

                if decrypted in encrypt_dicts[index]:
                    for k1 in encrypt_dicts[index][decrypted]:
                        if (k1, k2) not in key_pair_counts:
                            key_pair_counts[(k1, k2)] = 0
                        key_pair_counts[(k1, k2)] += 1

        # 寻找满足所有明密文对的k1和k2
        max_count = len(pairs)
        potential_key_pairs = []
        for key_pair, count in key_pair_counts.items():
            if count == max_count:
                potential_key_pairs.append(key_pair)

        if potential_key_pairs:
            return potential_key_pairs
        return None

    def split_text(self, num):
        return [str(hex(num))[i:i + 4] for i in range(2, len(str(num)), 4)]

    def CBC_encrypt(self, longtext, key, IV):
        texts = self.split_text(longtext)
        mids = []
        mids.append(IV)
        for i in range(len(texts)):
            if texts[i] != '':
                txt = int(texts[i], 16)
                txt = txt ^ mids[i]
                mids.append(self.encrypt(txt, key))
        ciphers = [hex(num)[2:] for num in mids[1:]]
        cipher = ''.join(ciphers)
        ciphertext = int(cipher, 16)
        return ciphertext

    def CBC_decrypt(self, longcipher, key, IV):
        cipher_parts = self.split_text(longcipher)
        cipher_parts = cipher_parts[::-1]
        cipher_parts.append(hex(IV))
        mids = []
        for i in range(len(cipher_parts) - 1):
            if cipher_parts[i] != '':
                cpr = int(cipher_parts[i], 16)
                mid_txt = self.decrypt(cpr, key)
                mid_txt = mid_txt ^ int(cipher_parts[i + 1], 16)
                mids.append(mid_txt)
        retext = [hex(num)[2:] for num in mids]
        retext = retext[::-1]
        plaintext = ''.join(retext)
        plaintext = int(plaintext, 16)
        return plaintext


if __name__ == "__main__":
    # print("Encrypting 0x0f0f with key 0x2D55")
    saes = SAES()
    # ciphertext = saes.encrypt(0x0f0f, 0x2D55)
    # print("Ciphertext: ", hex(ciphertext))
    # print("Ciphertext: ", bin(ciphertext))
    # plaintext = saes.decrypt(ciphertext, 0x2D55)
    # print("Plaintext: ", hex(plaintext))
    #
    # ciphertext_str = saes.encrypt_string("Hello World!", 0x2D55)
    # print("Encrypted string: ", ciphertext_str)
    # plaintext_str = saes.decrypt_string(ciphertext_str, 0x2D55)
    # print("Decrypted string: ", plaintext_str)
    #
    # # 明文：0000111100001111，密钥：0010110101010101
    # plaintext = 0x0f0f
    # key = 0x2D55
    # saes = SAES()
    # ciphertext = saes.encrypt(plaintext, key)
    # plaintext = saes.decrypt(ciphertext, key)
    # print("Ciphertext: ", bin(ciphertext))
    # print("Plaintext: ", bin(plaintext))
    #
    # # 加密函数 saes.encrypt(text, key)
    # # 解密函数 saes.decrypt(cipher, key)
    # plaintext = 0x0f00
    # double_key = 0x0000214a
    # cipher = saes.double_encrypt(plaintext, double_key)
    # retext = saes.double_decrypt(cipher, double_key)
    # print("double_encrypt_ciphertext:", hex(cipher))
    # print("double_decrypt_plaintext:", hex(retext))
    # # key = saes.MitMAttack(plaintext, cipher)
    # # print(hex(key))
    # tri_key = 0x111122223333
    # tcipher = saes.tri_encrypt(plaintext, tri_key)
    # tretext = saes.tri_decrypt(tcipher, tri_key)
    # print("tri_encrypt_ciphertext:", hex(tcipher))
    # print("tri_decrypt_plaintext:", hex(tretext))
    # print()
    #
    # import random
    #
    # plaintext = 0xf0ff123456789abcdef130b34e8a207d
    # print(hex(plaintext))
    # key = 0x2D55
    # IV = 0x3e8d
    # print(hex(IV))
    # cipher = saes.CBC_encrypt(plaintext, key, IV)
    # print(hex(cipher))
    # retext = saes.CBC_decrypt(cipher, key, IV)
    # print(hex(retext))
    # saes = SAES()
    # # 生成明密文对
    plaintext1 = 0x0f01
    key1 = 0xcd55
    key2 = 0xcd55
    # 将key1和key2转换成十进制
    ciphertext1 = saes.double_encrypt(plaintext1, key1, key2)

    plaintext2 = 0x0f00
    ciphertext2 = saes.double_encrypt(plaintext2, key1, key2)

    print("double_encrypt_ciphertext1:", hex(ciphertext1))
    print("double_encrypt_ciphertext2:", hex(ciphertext2))

    plaintext3 = 0x0f02
    ciphertext3 = saes.double_encrypt(plaintext3, key1, key2)
    print("double_encrypt_ciphertext3:", hex(ciphertext3))

    # 创建明密文对列表
    pairs = [
        {'plaintext': plaintext1, 'ciphertext': ciphertext1},
        {'plaintext': plaintext2, 'ciphertext': ciphertext2},
        {'plaintext': plaintext3, 'ciphertext': ciphertext3}
    ]

    # 调用MitMAttack
    recovered_keys = saes.MitMAttack(pairs)
    print(len(recovered_keys))
    for key in recovered_keys:
        print("Recovered key: ", hex(key[0]), hex(key[1]))
        print("Recovered key: ", bin(key[0]), bin(key[1]))

