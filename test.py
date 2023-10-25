from SAES import SAES

saes = SAES()

# key1 = 0xb5a9
# key2 = 0xf954
#
# plain = [0x0f00, 0x0f01, 0x0f02]
# for i in range(len(plain)):
#     print("Plain: ", hex(plain[i]))
#     cipher = saes.double_encrypt(plain[i], key1, key2)
#     print("Cipher: ", hex(cipher))
# # 将1101011100101100，0110110100111010，1111111100000000，0111011011110111转换成16进制
# plaintext1 = 0xd72c
# cypher1 = 0x6d3a
# plaintext2 = 0xff00
# cypher2 = 0x76f7
# pairs = [
#         {'plaintext': plaintext1, 'ciphertext': cypher1},
#         {'plaintext': plaintext2, 'ciphertext': cypher2}
#     ]
# recover_key = saes.MitMAttack(pairs)
# for key in recover_key:
#     print("Recovered key: ", hex(key[0]), hex(key[1]))

# # 将715a，e152转换成二进制
# plaintext1 = 0x715a
# print(bin(plaintext1))
# cypher1 = 0xe152
# print(bin(cypher1))
# print(bin(0x915c))

#"plainText": "1010000010100000",
        #"key1": "1010001110101111",
paintext = 0xa0a0
key1 = 0xa3af
c = saes.encrypt(paintext, key1)
print(hex(c))
print(bin(c))