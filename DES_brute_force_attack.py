import DES_en_de_crypt

#暴力破解
key = [0,1,0,1,1,0,1,0,1,0]
plaintext1=[1,1,1,1,1,1,1,1]
plaintext2=[1,1,1,1,1,1,1,0]
plaintext3=[1,1,1,1,1,1,0,1]
plaintext4=[1,1,1,1,1,1,0,0]

ciphertext1=[0,0,0,0,1,1,1,1]
ciphertext2=[0,1,1,1,0,1,1,0]
ciphertext3=[0,1,0,1,1,0,1,0]
ciphertext4=[0,1,1,1,1,1,0,1]
for i in range(1024):

    binary = bin(i)[2:].zfill(10)  # 将迭代变量转换为二进制字符串，并填充到10位
    new_key = key.copy()
    for j in range(10):
        new_key[j] = int(binary[j])  # 更新密钥的每一位
    ciphertext11=DES_en_de_crypt.encrypt(plaintext1,new_key)
    ciphertext12=DES_en_de_crypt.encrypt(plaintext2,new_key)
    ciphertext13=DES_en_de_crypt.encrypt(plaintext3,new_key)
    ciphertext14=DES_en_de_crypt.encrypt(plaintext4,new_key)

    if (ciphertext11 == ciphertext1).all() and (ciphertext12==ciphertext2).all() and (ciphertext13==ciphertext3).all() and (ciphertext14==ciphertext4).all():

       print(new_key)
       print(i)
    #else: 
     #  print("未找到")





