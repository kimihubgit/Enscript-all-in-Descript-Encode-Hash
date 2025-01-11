# hảm Encode Tiktok Email
def xor(string: str) -> str:
    return "".join([chr(int(string[i:i+2], 16) ^ 5) for i in range(0, len(string), 2)])

enc = '76767676456268646c692b666a68' #chuỗi mã hóa cần giải
dec = xor(enc)
print(dec)

# hàm decode tiktok email
def xor(string: str) -> str:
    return "".join([hex(ord(_) ^ 5)[2:] for _ in string]) 
    
dec='ssss@gmail.com' 
enc=xor(dec) 
print(enc)

