import numpy as np
# ip置换


def ip_permutation(plaintext):
    IP = np.array([2, 6, 3, 1, 4, 8, 5, 7])
    return [plaintext[i-1] for i in IP]


def ip_inverse_permutation(plaintext):
    IP_INV = np.array([4, 1, 3, 5, 7, 2, 8, 6])
    return [plaintext[i-1] for i in IP_INV]

# p10操作


def p10_permutation(key):
    P10 = np.array([3, 5, 2, 7, 4, 10, 1, 9, 8, 6])
    return [key[i-1] for i in P10]

# 左移一位


def left_shift(key, num_shifts):
    return key[num_shifts:] + key[:num_shifts]

# p8操作


def p8_permutation(key):
    P8 = np.array([6, 3, 7, 4, 8, 5, 10, 9])
    return [key[i-1] for i in P8]

# F函数


def ep_permutation(right_half):
    EP = np.array([4, 1, 2, 3, 2, 3, 4, 1])
    return [right_half[i-1] for i in EP]

# SP置换


def sp_permutation(s):
    SP_BOX = np.array([2, 4, 3, 1])
    sp_result = [s[SP_BOX[i]-1] for i in range(len(SP_BOX))]
    return np.array(sp_result)


# 求k1、k2
def generate_k1(encrypted_key):
    left_half = encrypted_key[:5]
    right_half = encrypted_key[5:]

    # 左移操作
    left_shifted_half = np.roll(left_half, -1)
    right_shifted_half = np.roll(right_half, -1)

    # 合并左右两部分
    before_k1 = np.concatenate((left_shifted_half, right_shifted_half))

    # P8 置换
    k1 = p8_permutation(before_k1)
    return k1


def generate_k2(encrypted_key):
    left_half = encrypted_key[:5]
    right_half = encrypted_key[5:]

    # 左移操作
    left_shifted_half = np.roll(left_half, -2)
    right_shifted_half = np.roll(right_half, -2)

    # 合并左右两部分
    before_k2 = np.concatenate((left_shifted_half, right_shifted_half))

    # P8 置换
    k2 = p8_permutation(before_k2)
    return k2

# 异或


def xor(arr1, arr2):
    return np.bitwise_xor(arr1, arr2)


def s_box(R1_eo_K1):
    left_half = R1_eo_K1[:4]
    right_half = R1_eo_K1[4:]
    SBOX1 = np.array([[1, 0, 3, 2],
                      [3, 2, 1, 0],
                      [0, 2, 1, 3],
                      [3, 1, 0, 2]])
    SBOX2 = np.array([[0, 1, 2, 3],
                      [2, 3, 1, 0],
                      [3, 0, 1, 2],
                      [2, 1, 0, 3]])
    SP_BOX = np.array([2, 4, 3, 1])

    # 拆分成左边两部分 (ab) 和 (cd)
    left_half = R1_eo_K1[:4]
    right_half = R1_eo_K1[4:]

    left_half1 = [left_half[1], left_half[2]]
    left_half2 = [left_half[0], left_half[3]]
    right_half1 = [right_half[1], right_half[2]]
    right_half2 = [right_half[0], right_half[3]]

    left_str1 = ''.join(map(str, left_half1))
    left_str2 = ''.join(map(str, left_half2))
    right_str1 = ''.join(map(str, right_half1))
    right_str2 = ''.join(map(str, right_half2))
    # 然后将每组二进制数转化为十进制数，也就是 S 盒中的行列索引
    left_decimal1 = int(left_str1, 2)
    left_decimal2 = int(left_str2, 2)
    right_decimal1 = int(right_str1, 2)
    right_decimal2 = int(right_str2, 2)

    # 找到对应的 s_left 值
    s_left = SBOX1[left_decimal2][left_decimal1]
    s_right = SBOX2[right_decimal2][right_decimal1]
    # 将 s_left 转换为两个bit，存在 s_left_1 中
    s_left_1 = [int(b) for b in "{0:02b}".format(s_left)]
    s_right_1 = [int(b) for b in "{0:02b}".format(s_right)]
    # 将 s_left_1 和 s_right_1 拼接成一个长度为4的二进制数
    F1 = s_left_1 + s_right_1
    F_SP1 = [F1[SP_BOX[i]-1] for i in range(len(SP_BOX))]

    return np.array(F_SP1)


def encrypt(plaintext, key):
    # 密钥侧处理
    encrypted_key = p10_permutation(key)
    LS1 = np.array([2, 3, 4, 5, 1])
    LS2 = np.array([3, 4, 5, 1, 2])

    k1 = [int(bit) for bit in generate_k1(encrypted_key)]
    k2 = [int(bit) for bit in generate_k2(encrypted_key)]

    # 初始置换IP
    encrypted_plaintext = ip_permutation(plaintext)
    left_half = encrypted_plaintext[:4]
    right_half = encrypted_plaintext[4:]
    # 第一轮
    expanded_right_half = ep_permutation(right_half)
    R1_xor_K1 = xor(expanded_right_half, k1)
    F1 = s_box(R1_xor_K1)
    left_half1 = xor(left_half, F1)
    # 左右交换
    temp1 = left_half1
    left_half2 = right_half
    right_half2 = temp1
    # 第二轮
    expanded_right_half2 = ep_permutation(right_half2)
    R2_xor_K2 = xor(expanded_right_half2, k2)
    F2 = s_box(R2_xor_K2)
    left_half3 = xor(left_half2, F2)
    before_ciphertext = []
    before_ciphertext.extend(left_half3)
    before_ciphertext.extend(right_half2)
    # ip逆得到密文
    ciphertext = ip_inverse_permutation(before_ciphertext)

    return np.array(ciphertext)

def encrypt2(plaintext, key):
    # 密钥侧处理
    encrypted_key = p10_permutation(key)
    LS1 = np.array([2, 3, 4, 5, 1])
    LS2 = np.array([3, 4, 5, 1, 2])

    k1 = generate_k1(encrypted_key)
    k2 = generate_k2(encrypted_key)

    # 初始置换IP
    plaintext = [int(bit) for bit in plaintext]
    encrypted_plaintext = ip_permutation(plaintext)
    left_half = encrypted_plaintext[:4]
    right_half = encrypted_plaintext[4:]
    # 第一轮
    expanded_right_half = ep_permutation(right_half)
    R1_xor_K1 = xor(expanded_right_half, k1)
    F1 = s_box(R1_xor_K1)
    left_half1 = xor(left_half, F1)
    # 左右交换
    temp1 = left_half1
    left_half2 = right_half
    right_half2 = temp1
    # 第二轮
    expanded_right_half2 = ep_permutation(right_half2)
    R2_xor_K2 = xor(expanded_right_half2, k2)
    F2 = s_box(R2_xor_K2)
    left_half3 = xor(left_half2, F2)
    before_ciphertext = []
    before_ciphertext.extend(left_half3)
    before_ciphertext.extend(right_half2)
    # ip逆得到密文
    ciphertext = ip_inverse_permutation(before_ciphertext)

    return np.array(ciphertext)

def decrypt(ciphertext, key):

    # 密钥侧处理
    encrypted_key = p10_permutation(key)
    LS1 = np.array([2, 3, 4, 5, 1])
    LS2 = np.array([3, 4, 5, 1, 2])

    k1 = [int(bit) for bit in generate_k1(encrypted_key)]
    k2 = [int(bit) for bit in generate_k2(encrypted_key)]
    # 初始置换IP
    ciphertext = ip_permutation(ciphertext)
    left_half = ciphertext[:4]
    right_half = ciphertext[4:]

    # 第一轮解密
    expanded_right_half = ep_permutation(right_half)
    R1_xor_K1 = xor(expanded_right_half, k2)
    F1 = s_box(R1_xor_K1)
    left_half1 = xor(left_half, F1)

    # 左右交换
    left_half2 = right_half
    right_half2 = left_half1

    # 第二轮解密
    expanded_right_half2 = ep_permutation(right_half2)
    R2_xor_K2 = xor(expanded_right_half2, k1)
    F2 = s_box(R2_xor_K2)
    left_half3 = xor(left_half2, F2)

    # 重组
    before_plaintext = []
    before_plaintext.extend(left_half3)
    before_plaintext.extend(right_half2)

    # IP逆置换得到明文
    plaintext = ip_inverse_permutation(before_plaintext)

    return np.array(plaintext)

def decrypt2(ciphertext, key):

    # 密钥侧处理
    encrypted_key = p10_permutation(key)
    LS1 = np.array([2, 3, 4, 5, 1])
    LS2 = np.array([3, 4, 5, 1, 2])

    k1 = generate_k1(encrypted_key)
    k2 = generate_k2(encrypted_key)
    # 初始置换IP
    ciphertext = [int(bit) for bit in ciphertext]
    ciphertext = ip_permutation(ciphertext)
    left_half = ciphertext[:4]
    right_half = ciphertext[4:]

    # 第一轮解密
    expanded_right_half = ep_permutation(right_half)
    R1_xor_K1 = xor(expanded_right_half, k2)
    F1 = s_box(R1_xor_K1)
    left_half1 = xor(left_half, F1)

    # 左右交换
    left_half2 = right_half
    right_half2 = left_half1

    # 第二轮解密
    expanded_right_half2 = ep_permutation(right_half2)
    R2_xor_K2 = xor(expanded_right_half2, k1)
    F2 = s_box(R2_xor_K2)
    left_half3 = xor(left_half2, F2)

    # 重组
    before_plaintext = []
    before_plaintext.extend(left_half3)
    before_plaintext.extend(right_half2)

    # IP逆置换得到明文
    plaintext = ip_inverse_permutation(before_plaintext)

    return np.array(plaintext)

"""
ciphertext = [1, 0, 1, 1, 0, 1, 1, 0]  # 示例密文
plaintext = [1, 1, 1, 1, 1, 1, 1, 1]  # 示例明文
key = [0, 1, 0, 1, 1, 0, 1, 0, 1, 0]  # 示例密钥


# 解密过程
decrypted_plaintext = decrypt(ciphertext, key)
encrypted_ciphertext = encrypt(plaintext, key)
print("解密后的明文：", decrypted_plaintext)
print("加密后的密文：", encrypted_ciphertext)
"""




     