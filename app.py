import streamlit as st
import numpy as np

# PAGE CONFIG

st.set_page_config(
    page_title="Hill Cipher Tool",
    page_icon="🔐",
    layout="centered"
)


# CUSTOM CSS

st.markdown("""
<style>

body{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

.main-title{
text-align:center;
font-size:40px;
font-weight:bold;
color:white;
margin-bottom:10px;
}

.sub-title{
text-align:center;
color:#d0d0d0;
margin-bottom:40px;
}

.card{
background: rgba(255,255,255,0.08);
padding:30px;
border-radius:20px;
backdrop-filter: blur(10px);
box-shadow:0 8px 32px rgba(0,0,0,0.3);
}

.result-box{
background:#111;
color:#00ff9f;
padding:20px;
border-radius:10px;
font-size:22px;
text-align:center;
margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# TITLE

st.markdown('<div class="main-title">🔐 Hill Cipher Encryption Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Python + Linear Algebra + Cryptography</div>', unsafe_allow_html=True)

# FUNCTIONS

def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]

def numbers_to_text(numbers):
    return ''.join(chr(int(num) + ord('A')) for num in numbers)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None



# ENCRYPT

def encrypt(plaintext, key_matrix, size):

    plaintext = plaintext.upper().replace(" ", "")

    while len(plaintext) % size != 0:
        plaintext += 'X'

    cipher_text = ""

    for i in range(0, len(plaintext), size):

        block = text_to_numbers(plaintext[i:i+size])
        block_matrix = np.array(block).reshape(size,1)

        result = np.dot(key_matrix, block_matrix) % 26

        cipher_text += numbers_to_text(result.flatten())

    return cipher_text


# DECRYPT

def decrypt(ciphertext, key_matrix, size):

    det = int(round(np.linalg.det(key_matrix)))
    det_mod = det % 26
    det_inv = mod_inverse(det_mod,26)

    if det_inv is None:
        return "Key matrix not invertible!"

    adjugate = np.round(det * np.linalg.inv(key_matrix)).astype(int)

    key_inverse = (det_inv * adjugate) % 26

    plaintext = ""

    for i in range(0,len(ciphertext),size):

        block = text_to_numbers(ciphertext[i:i+size])
        block_matrix = np.array(block).reshape(size,1)

        result = np.dot(key_inverse,block_matrix) % 26

        plaintext += numbers_to_text(result.flatten())

    return plaintext


# UI CARD

st.markdown('<div class="card">', unsafe_allow_html=True)

size = st.selectbox("Select Matrix Size", [2,3])

st.subheader("Key Matrix")

key = []

if size == 2:

    col1,col2 = st.columns(2)

    with col1:
        a = st.number_input("K[0][0]",value=2)
        c = st.number_input("K[1][0]",value=1)

    with col2:
        b = st.number_input("K[0][1]",value=3)
        d = st.number_input("K[1][1]",value=3)

    key_matrix = np.array([[a,b],[c,d]])

else:

    cols = st.columns(3)

    for i in range(3):
        row=[]
        for j in range(3):
            row.append(cols[j].number_input(f"K[{i}][{j}]",value=1))
        key.append(row)

    key_matrix = np.array(key)

operation = st.radio("Operation",["Encrypt","Decrypt"])

text = st.text_input("Enter Text")

run = st.button("🚀 Run Cipher")

st.markdown('</div>', unsafe_allow_html=True)

# RUN

if run:

    if operation=="Encrypt":
        result = encrypt(text,key_matrix,size)
    else:
        result = decrypt(text,key_matrix,size)

    st.markdown(f'<div class="result-box">Result: {result}</div>', unsafe_allow_html=True)
