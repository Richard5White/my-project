import tkinter as tk
from tkinter import messagebox
import DES_en_de_crypt


# 加密按钮点击事件处理函数
def encrypt_button_clicked():
    plaintext = plaintext_entry.get()
    key = key_entry.get()

    # 判断传入明文和密钥是否都是字符（1字节）
    if len(plaintext) == 1 and len(key) == 1:
        plaintext_ascii = ord(plaintext)
        key_ascii = ord(key)

        # 判断如果明密文的ascii码大于255或者密钥的ascii码大于1023，则提示“请输入正确的ascii码”
        if plaintext_ascii > 255 or key_ascii > 1023:
            messagebox.showerror("错误", "请输入正确的ascii码")
        else:
            plaintext_binary = format(plaintext_ascii, '08b')  # 将明文转化为8bit二进制list
            plaintext = [int(bit) for bit in plaintext_binary]
            key_binary = format(key_ascii, '010b')  # 将密钥转化为10bit的二进制字符串
            key = [int(bit) for bit in key_binary]

            # 调用加密函数
            #ciphertext = DES01decrypt.encrypt(plaintext, key)
            #ciphertext_entry.delete(0, tk.END)
            #ciphertext_entry.insert(0, "".join(str(bit) for bit in ciphertext))
            ciphertext = DES_en_de_crypt.encrypt(plaintext, key)
            ciphertext_chars = ""
            for i in range(0, len(ciphertext), 8):
                binary = ciphertext[i:i+8]
                decimal = int("".join(str(bit) for bit in binary), 2)
                if decimal > 127:
                   # 如果超出了ascii码能表示的范围，直接显示二进制形式的密文
                   ciphertext_entry.delete(0, tk.END)
                   ciphertext_entry.insert(0, "".join(str(bit) for bit in ciphertext))
                   return
                character = chr(decimal)
                ciphertext_chars += character
            ciphertext_entry.delete(0, tk.END)
            ciphertext_entry.insert(0, ciphertext_chars)
            
            

    # 判断传入明文是8bit且密钥是10bit
    elif len(plaintext) == 8 and len(key) == 10:
        plaintext_binary = [int(bit) for bit in plaintext]
        key_binary = [int(bit) for bit in key]

        # 检查明文、密钥是否只由0和1构成
        if set(plaintext) <= {'0', '1'} and set(key) <= {'0', '1'}:
            # 调用加密函数
            ciphertext = DES_en_de_crypt.encrypt(plaintext_binary, key_binary)
            ciphertext_entry.delete(0, tk.END)
            ciphertext_entry.insert(0, "".join(str(bit) for bit in ciphertext))
        else:
            messagebox.showerror("错误", "请注意输入是否正确")

    # 判断传入明文是8bit且密钥是字符（1字节）
    elif len(plaintext) == 8 and len(key) == 1:
        key_ascii = ord(key)

        # 判断如果密钥的ascii码不大于1023或者明文只由0和1构成，则将密钥的ascii码转化为10bit的二进制字符串，然后调用加密函数
        if key_ascii > 1023 and set(plaintext) <= {'0', '1'}:
            messagebox.showerror("错误", "请输入正确的ascii码")
        else:
            key_binary = format(key_ascii, '010b')  # 将密钥转化为10bit的二进制字符串
            key = [int(bit) for bit in key_binary]

            # 调用加密函数
            ciphertext = DES_en_de_crypt.encrypt2(plaintext, key)
            ciphertext_entry.delete(0, tk.END)
            ciphertext_entry.insert(0, "".join(str(bit) for bit in ciphertext))

    # 判断传入明文是字符（1字节）且密钥是10bit
    elif len(plaintext) == 1 and len(key) == 10:
        plaintext_ascii = ord(plaintext)
        plaintext_binary = format(plaintext_ascii, '08b')  # 将明文转化为8bit二进制字符串
        plaintext_binary_str = str(plaintext_binary)  # 将二进制字符串转换为普通字符串
        print(plaintext_binary_str)
        # 判断如果明文的ascii码不大于255且密钥只由0和1构成，则将明文的ascii码转化为8bit的二进制字符串，再调用加密函数
        if plaintext_ascii > 255:#or set(key) <= {'0', '1'}:
            messagebox.showerror("错误", "请输入正确的ascii码")
        else:

            plaintext = [int(bit) for bit in plaintext_binary]

            ciphertext = DES_en_de_crypt.encrypt(plaintext, key)
            #ciphertext_entry.delete(0, tk.END)
            #ciphertext_entry.insert(0, "".join(str(bit) for bit in ciphertext))

            """
            ciphertext = DES01decrypt.encrypt(plaintext, key)
            ciphertext_chars = ""
            for i in range(0, len(ciphertext), 8):
                binary = ciphertext[i:i+8]
                decimal = int("".join(str(bit) for bit in binary), 2)
                character = chr(decimal)
                ciphertext_chars += character
            ciphertext_entry.delete(0, tk.END)
            ciphertext_entry.insert(0, ciphertext_chars)
            """
            ciphertext_chars = ""
            for i in range(0, len(ciphertext), 8):
                binary = ciphertext[i:i+8]
                decimal = int("".join(str(bit) for bit in binary), 2)
                if decimal > 127:
                   # 如果超出了ascii码能表示的范围，直接显示二进制形式的密文
                   ciphertext_entry.delete(0, tk.END)
                   ciphertext_entry.insert(0, "".join(str(bit) for bit in ciphertext))
                   return
                character = chr(decimal)
                ciphertext_chars += character
            ciphertext_entry.delete(0, tk.END)
            ciphertext_entry.insert(0, ciphertext_chars)


    # 其他输入情况则提示“请注意输入是否正确”
    else:
        messagebox.showerror("错误", "请注意输入是否正确")





def decrypt_button_clicked():
    ciphertext = ciphertext_entry.get()
    key = key_entry.get()

    # 判断传入明文和密钥是否都是字符（1字节）
    if len(ciphertext) == 1 and len(key) == 1:
        ciphertext_ascii = ord(ciphertext)
        key_ascii = ord(key)

        # 判断如果明密文的ascii码大于255或者密钥的ascii码大于1023，则提示“请输入正确的ascii码”
        if ciphertext_ascii > 255 or key_ascii > 1023:
            messagebox.showerror("错误", "请输入正确的ascii码")
        else:
            ciphertext_binary = format(ciphertext_ascii, '08b')  # 将密文转化为8bit二进制list
            ciphertext = [int(bit) for bit in ciphertext_binary]
            key_binary = format(key_ascii, '010b')  # 将密钥转化为10bit的二进制字符串
            key = [int(bit) for bit in key_binary]

            # 调用解密函数
            #plaintext = DES01decrypt.decrypt(ciphertext, key)
            #plaintext_entry.delete(0, tk.END)
            #plaintext_entry.insert(0, "".join(str(bit) for bit in plaintext))

            plaintext = DES_en_de_crypt.decrypt(ciphertext, key)
            """
            plaintext_chars = ""
            for i in range(0, len(plaintext), 8):
                binary = plaintext[i:i+8]
                decimal = int("".join(str(bit) for bit in binary), 2)
                character = chr(decimal)
                plaintext_chars += character
            plaintext_entry.delete(0, tk.END)
            plaintext_entry.insert(0, plaintext_chars)    
            """       

            plaintext_chars = ""
            for i in range(0, len(plaintext), 8):
                binary = plaintext[i:i+8]
                decimal = int("".join(str(bit) for bit in binary), 2)
                if decimal > 127:
                   # 如果超出了ascii码能表示的范围，直接显示二进制形式的密文
                   ciphertext_entry.delete(0, tk.END)
                   ciphertext_entry.insert(0, "".join(str(bit) for bit in plaintext))
                   return
                character = chr(decimal)
                plaintext_chars += character
            plaintext_entry.delete(0, tk.END)
            plaintext_entry.insert(0, plaintext_chars)



    # 判断传入明文是8bit且密钥是10bit
    elif len(ciphertext) == 8 and len(key) == 10:
        ciphertext_binary = [int(bit) for bit in ciphertext]
        key_binary = [int(bit) for bit in key]

        # 检查密文、密钥是否只由0和1构成
        if set(ciphertext) <= {'0', '1'} and set(key) <= {'0', '1'}:
            # 调用解密函数
            plaintext = DES_en_de_crypt.decrypt(ciphertext_binary, key_binary)
            plaintext_entry.delete(0, tk.END)
            plaintext_entry.insert(0, "".join(str(bit) for bit in plaintext))
        else:
            messagebox.showerror("错误", "请注意输入是否正确")

    # 判断传入密文是8bit且密钥是字符（1字节）
    elif len(ciphertext) == 8 and len(key) == 1:
        key_ascii = ord(key)

        # 判断如果密钥的ascii码不大于1023或者明文只由0和1构成，则将密钥的ascii码转化为10bit的二进制字符串，然后调用加密函数
        if key_ascii > 1023 and set(ciphertext) <= {'0', '1'}:
            messagebox.showerror("错误", "请输入正确的ascii码")
        else:
            key_binary = format(key_ascii, '010b')  # 将密钥转化为10bit的二进制字符串
            key = [int(bit) for bit in key_binary]

            # 调用解密函数
            plaintext = DES_en_de_crypt.decrypt2(ciphertext, key)
            plaintext_entry.delete(0, tk.END)
            plaintext_entry.insert(0, "".join(str(bit) for bit in plaintext))

    # 判断传入密文是字符（1字节）且密钥是10bit
    elif len(ciphertext) == 1 and len(key) == 10:
        ciphertext_ascii = ord(ciphertext)
        ciphertext_binary = format(ciphertext_ascii, '08b')  # 将明文转化为8bit二进制字符串
        # 判断如果密文的ascii码不大于255且密钥只由0和1构成，则将明文的ascii码转化为8bit的二进制字符串，再调用加密函数
        if ciphertext_ascii > 255:#or set(key) <= {'0', '1'}:
            messagebox.showerror("错误", "请输入正确的ascii码")
        else:

            ciphertext = [int(bit) for bit in ciphertext_binary]
            #plaintext = DES01decrypt.decrypt(ciphertext, key)
            #plaintext_entry.delete(0, tk.END)
            #plaintext_entry.insert(0, "".join(str(bit) for bit in plaintext))

            plaintext = DES_en_de_crypt.decrypt(ciphertext, key)
            plaintext_chars = ""
            for i in range(0, len(plaintext), 8):
                binary = plaintext[i:i+8]
                decimal = int("".join(str(bit) for bit in binary), 2)
                if decimal > 127:
                   # 如果超出了ascii码能表示的范围，直接显示二进制形式的密文
                   ciphertext_entry.delete(0, tk.END)
                   ciphertext_entry.insert(0, "".join(str(bit) for bit in plaintext))
                   return
                character = chr(decimal)
                plaintext_chars += character
            plaintext_entry.delete(0, tk.END)
            plaintext_entry.insert(0, plaintext_chars)  


    # 其他输入情况则提示“请注意输入是否正确”
    else:
        messagebox.showerror("错误", "请注意输入是否正确")


# 创建主窗口
window = tk.Tk()
window.title("DES加解密工具")

# 设置窗口大小和背景颜色
window.geometry("380x200")
window.configure(bg="#F9F9F9")

# 创建输入框和标签
plaintext_label = tk.Label(window, text="明文（8位）：", font=("微软雅黑", 12), bg="#F9F9F9")
plaintext_entry = tk.Entry(window, font=("微软雅黑", 12), width=20, bd=2)

ciphertext_label = tk.Label(window, text="密文（8位）：", font=("微软雅黑", 12), bg="#F9F9F9")
ciphertext_entry = tk.Entry(window, font=("微软雅黑", 12), width=20, bd=2)

key_label = tk.Label(window, text="密钥（10位）：", font=("微软雅黑", 12), bg="#F9F9F9")
key_entry = tk.Entry(window, font=("微软雅黑", 12), width=20, bd=2)

# 创建按钮
encrypt_button = tk.Button(window, text="加密", font=("微软雅黑", 12), bg="#4AAE9B", fg="#FFFFFF", command=encrypt_button_clicked)
decrypt_button = tk.Button(window, text="解密", font=("微软雅黑", 12), bg="#DF5E88", fg="#FFFFFF", command=decrypt_button_clicked)

# 设置布局
plaintext_label.grid(row=0, column=0, padx=20, pady=10)
plaintext_entry.grid(row=0, column=1, padx=20, pady=10)

ciphertext_label.grid(row=1, column=0, padx=20, pady=10)
ciphertext_entry.grid(row=1, column=1, padx=20, pady=10)

key_label.grid(row=2, column=0, padx=20, pady=10)
key_entry.grid(row=2, column=1, padx=20, pady=10)

encrypt_button.grid(row=3, column=0, padx=20, pady=10)
decrypt_button.grid(row=3, column=1, padx=20, pady=10)


# 运行主循环
window.mainloop()
