<<<<<<< HEAD
<<<<<<< HEAD
def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def key_to_binary(key):
    hex_key = key.replace(" ", "")
    binary_key = bin(int(hex_key, 16))[2:].zfill(64)
    return binary_key

def binary_to_hex(binary_str):
    hex_str = hex(int(binary_str, 2))[2:]
    return hex_str.upper()

def permute(text, permutation_table):
    permuted_text = ''.join(text[index - 1] for index in permutation_table)
    return permuted_text

plainText = "subagdja"
key = "FF 0A 02 FF FF FF 01 A1"
l = []
r = []
c = []
d = []
cd = []

# Tabel permutasi untuk plaintext dalam DES
plaintext_permutation_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Tabel permutasi PC-1 untuk kunci dalam DES
pc1_key_permutation_table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Tabel permutasi PC-2 untuk kunci dalam DES
pc2_key_permutation_table = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

expansion_table = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

p_box_table = [
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

# Tabel permutasi invers IP-1 untuk algoritma DES
ip_inverse_permutation_table = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
]

def substitute_sbox(block):
    sbox_tables = [
        # S-box 1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S-box 2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S-box 3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S-box 4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S-box 5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S-box 6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S-box 7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S-box 8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    result = ""
    for i in range(0, 48, 6):
        block_chunk = block[i:i+6]
        row = int(block_chunk[0] + block_chunk[5], 2)
        col = int(block_chunk[1:5], 2)
        sbox_value = sbox_tables[i // 6][row][col]
        result += format(sbox_value, '04b')  # Mengonversi nilai S-box ke dalam biner 4-bit
    
    return result

binary_plainText = text_to_binary(plainText)
binary_key = key_to_binary(key)

permuted_plainText = permute(binary_plainText, plaintext_permutation_table)
permuted_key = permute(binary_key, pc1_key_permutation_table)

half = len(permuted_plainText)//2

l.append(permuted_plainText[:half])
r.append(permuted_plainText[half:])

half_key = len(permuted_key) // 2

c.append(permuted_key[:half_key])
d.append(permuted_key[half_key:])
cd.append(c[0] + d[0])

print("PlainText (Binary):", binary_plainText)
print("Key (Binary):", binary_key)
print("\nPermuted PlainText:", permuted_plainText)
print("L : ", l)
print("R : ", r)
print("\nPermuted Key:", permuted_key)
print("C : ", c)
print("D : ", d)

perputaran_bit = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

for index, rotation in enumerate(perputaran_bit):
    # Lakukan rotasi pada C dan D   
    c_new = c[index][rotation:] + c[index][:rotation]
    d_new = d[index][rotation:] + d[index][:rotation]
    
    # Tambahkan hasil rotasi ke dalam list
    c.append(c_new)
    d.append(d_new)
    cd.append(c_new +  d_new)

for i in range(0, 17):
    print("CD[]",  c[i], d[i], sep=", ")
    # print("CD[", i, "]", cd[i])

print("\nHasil Permutasi PC-2")

k = []
k.append(permute(cd[0], pc2_key_permutation_table))

for i in range(1, 17):
    permuted_plainText_pc2 = permute(cd[i], pc2_key_permutation_table)
    k.append(permuted_plainText_pc2)  # Simpan nilai K hasil permutasi PC-2
    print("CD[", i, "] : ", cd[i], sep="")
    print("K[", i, "]  : ", k[i], sep="")

print("\n#Langkah 5")

e = []
a = []
b = []
p = []

e.append(0)
a.append(0)
b.append(0)
p.append(0)

# print("\ne", e)
# print("\na", a)
# print("\nb", b)
# print("\np", p)
# print("\np", l)
# print("\np", k)

for i in range(1, 17):
    e.append(permute(r[i-1], expansion_table))
    result = ''.join(str(int(e_bit) ^ int(k_bit)) for e_bit, k_bit in zip(e[i], k[i]))
    a.append(result)
    b.append(substitute_sbox(a[i]))
    p.append(permute(b[i], p_box_table))
    if (i == 1):
        l.append(l[0])
    elif (i == 2):
        l.append(r[0])
    else:
        l.append(r[i-2])

    xor_result = ''.join(str(int(p_bit) ^ int(l_bit)) for p_bit, l_bit in zip(p[i], l[i]))
    r.append(xor_result)

    print("\nE[{}]: {}".format(i, e[i]))
    print("K[{}]: {}".format(i, k[i]))
    print("A[{}]: {}".format(i, a[i]))
    print("B[{}]: {}".format(i, b[i]))
    print("P(B)[{}]: {}".format(i, p[i]))
    print("L[{}]: {}".format(i, l[i]))
    print("R[{}]: {}".format(i, r[i]))

print("\nFinal L dan R :")
print("L[16] :", r[15])
print("R[16] :", r[16])

rl = r[16] + r[15]
print("R[16]L[16] Adalah : ", rl)

cipher = permute(rl, ip_inverse_permutation_table)
print("Hasil Akhir Adalah : ", cipher)

cipher_hex = binary_to_hex(cipher)
=======
def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def key_to_binary(key):
    hex_key = key.replace(" ", "")
    binary_key = bin(int(hex_key, 16))[2:].zfill(64)
    return binary_key

def binary_to_hex(binary_str):
    hex_str = hex(int(binary_str, 2))[2:]
    return hex_str.upper()

def permute(text, permutation_table):
    permuted_text = ''.join(text[index - 1] for index in permutation_table)
    return permuted_text

plainText = "subagdja"
key = "13 34 57 79 9B BC DF F1"
l = []
r = []
c = []
d = []
cd = []

# Tabel permutasi untuk plaintext dalam DES
plaintext_permutation_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Tabel permutasi PC-1 untuk kunci dalam DES
pc1_key_permutation_table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Tabel permutasi PC-2 untuk kunci dalam DES
pc2_key_permutation_table = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

expansion_table = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

p_box_table = [
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

# Tabel permutasi invers IP-1 untuk algoritma DES
ip_inverse_permutation_table = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
]

def substitute_sbox(block):
    sbox_tables = [
        # S-box 1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S-box 2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S-box 3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S-box 4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S-box 5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S-box 6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S-box 7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S-box 8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    result = ""
    for i in range(0, 48, 6):
        block_chunk = block[i:i+6]
        row = int(block_chunk[0] + block_chunk[5], 2)
        col = int(block_chunk[1:5], 2)
        sbox_value = sbox_tables[i // 6][row][col]
        result += format(sbox_value, '04b')  # Mengonversi nilai S-box ke dalam biner 4-bit
    
    return result

binary_plainText = text_to_binary(plainText)
binary_key = key_to_binary(key)

permuted_plainText = permute(binary_plainText, plaintext_permutation_table)
permuted_key = permute(binary_key, pc1_key_permutation_table)

half = len(permuted_plainText)//2

l.append(permuted_plainText[:half])
r.append(permuted_plainText[half:])

half_key = len(permuted_key) // 2

c.append(permuted_key[:half_key])
d.append(permuted_key[half_key:])
cd.append(c[0] + d[0])

print("PlainText (Binary):", binary_plainText)
print("Key (Binary):", binary_key)
print("\nPermuted PlainText:", permuted_plainText)
print("L : ", l)
print("R : ", r)
print("\nPermuted Key:", permuted_key)
print("C : ", c)
print("D : ", d)

perputaran_bit = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

for index, rotation in enumerate(perputaran_bit):
    # Lakukan rotasi pada C dan D   
    c_new = c[index][rotation:] + c[index][:rotation]
    d_new = d[index][rotation:] + d[index][:rotation]
    
    # Tambahkan hasil rotasi ke dalam list
    c.append(c_new)
    d.append(d_new)
    cd.append(c_new + d_new)

print("Biar tau panjang : ", len(cd))

for i in range(0, 17):
    print("CD[", i, "]", cd[i])

print("Hasil Permutasi PC-2")

k = []
k.append(permute(cd[0], pc2_key_permutation_table))

for i in range(1, 17):
    permuted_plainText_pc2 = permute(cd[i], pc2_key_permutation_table)
    k.append(permuted_plainText_pc2)  # Simpan nilai K hasil permutasi PC-2
    print("CD :", cd[i])
    print("K-", i, ":", k[i], "Len", len(k[i]))

print("\n#Langkah 5")

e = []
a = []
b = []
p = []

e.append(0)
a.append(0)
b.append(0)
p.append(0)

# print("\ne", e)
# print("\na", a)
# print("\nb", b)
# print("\np", p)
# print("\np", l)
# print("\np", k)

for i in range(1, 17):
    e.append(permute(r[i-1], expansion_table))
    result = ''.join(str(int(e_bit) ^ int(k_bit)) for e_bit, k_bit in zip(e[i], k[i]))
    a.append(result)
    b.append(substitute_sbox(a[i]))
    p.append(permute(b[i], p_box_table))
    if (i == 1):
        l.append(l[0])
    elif (i == 2):
        l.append(r[0])
    else:
        l.append(r[i-2])

    xor_result = ''.join(str(int(p_bit) ^ int(l_bit)) for p_bit, l_bit in zip(p[i], l[i]))
    r.append(xor_result)

    print("\ne[{}]: {}".format(i, e[i]))
    print("k[{}]: {}".format(i, k[i]))
    print("Ai :", a[i])
    print("Sbox :", b[i])
    print("P(B) : ", p[i])
    print("Li : ", l[i])
    print("Ri:", r[i])

print("\nFinal L dan R :")
print("L-16 :", r[15])
print("R-16 :", r[16])

rl = r[16] + r[15]
print("RL Adalah : ", rl)

cipher = permute(rl, ip_inverse_permutation_table)
print("Hasil Akhir Adalah : ", cipher)

cipher_hex = binary_to_hex(cipher)
>>>>>>> ef1b5081676c197bb8813f4d0c114f8f27199269
=======
def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def key_to_binary(key):
    hex_key = key.replace(" ", "")
    binary_key = bin(int(hex_key, 16))[2:].zfill(64)
    return binary_key

def binary_to_hex(binary_str):
    hex_str = hex(int(binary_str, 2))[2:]
    return hex_str.upper()

def permute(text, permutation_table):
    permuted_text = ''.join(text[index - 1] for index in permutation_table)
    return permuted_text

plainText = "subagdja"
key = "FF 0A 02 FF FF FF 01 A1"
l = []
r = []
c = []
d = []
cd = []

# Tabel permutasi untuk plaintext dalam DES
plaintext_permutation_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Tabel permutasi PC-1 untuk kunci dalam DES
pc1_key_permutation_table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Tabel permutasi PC-2 untuk kunci dalam DES
pc2_key_permutation_table = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

expansion_table = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

p_box_table = [
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

# Tabel permutasi invers IP-1 untuk algoritma DES
ip_inverse_permutation_table = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
]

def substitute_sbox(block):
    sbox_tables = [
        # S-box 1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S-box 2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S-box 3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S-box 4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S-box 5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S-box 6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S-box 7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S-box 8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    result = ""
    for i in range(0, 48, 6):
        block_chunk = block[i:i+6]
        row = int(block_chunk[0] + block_chunk[5], 2)
        col = int(block_chunk[1:5], 2)
        sbox_value = sbox_tables[i // 6][row][col]
        result += format(sbox_value, '04b')  # Mengonversi nilai S-box ke dalam biner 4-bit
    
    return result

binary_plainText = text_to_binary(plainText)
binary_key = key_to_binary(key)

permuted_plainText = permute(binary_plainText, plaintext_permutation_table)
permuted_key = permute(binary_key, pc1_key_permutation_table)

half = len(permuted_plainText)//2

l.append(permuted_plainText[:half])
r.append(permuted_plainText[half:])

half_key = len(permuted_key) // 2

c.append(permuted_key[:half_key])
d.append(permuted_key[half_key:])
cd.append(c[0] + d[0])

print("PlainText (Binary):", binary_plainText)
print("Key (Binary):", binary_key)
print("\nPermuted PlainText:", permuted_plainText)
print("L : ", l)
print("R : ", r)
print("\nPermuted Key:", permuted_key)
print("C : ", c)
print("D : ", d)

perputaran_bit = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

for index, rotation in enumerate(perputaran_bit):
    # Lakukan rotasi pada C dan D   
    c_new = c[index][rotation:] + c[index][:rotation]
    d_new = d[index][rotation:] + d[index][:rotation]
    
    # Tambahkan hasil rotasi ke dalam list
    c.append(c_new)
    d.append(d_new)
    cd.append(c_new +  d_new)

for i in range(0, 17):
    print("CD[]",  c[i], d[i], sep=", ")
    # print("CD[", i, "]", cd[i])

print("\nHasil Permutasi PC-2")

k = []
k.append(permute(cd[0], pc2_key_permutation_table))

for i in range(1, 17):
    permuted_plainText_pc2 = permute(cd[i], pc2_key_permutation_table)
    k.append(permuted_plainText_pc2)  # Simpan nilai K hasil permutasi PC-2
    print("CD[", i, "] : ", cd[i], sep="")
    print("K[", i, "]  : ", k[i], sep="")

print("\n#Langkah 5")

e = []
a = []
b = []
p = []

e.append(0)
a.append(0)
b.append(0)
p.append(0)

# print("\ne", e)
# print("\na", a)
# print("\nb", b)
# print("\np", p)
# print("\np", l)
# print("\np", k)

for i in range(1, 17):
    e.append(permute(r[i-1], expansion_table))
    result = ''.join(str(int(e_bit) ^ int(k_bit)) for e_bit, k_bit in zip(e[i], k[i]))
    a.append(result)
    b.append(substitute_sbox(a[i]))
    p.append(permute(b[i], p_box_table))
    if (i == 1):
        l.append(l[0])
    elif (i == 2):
        l.append(r[0])
    else:
        l.append(r[i-2])

    xor_result = ''.join(str(int(p_bit) ^ int(l_bit)) for p_bit, l_bit in zip(p[i], l[i]))
    r.append(xor_result)

    print("\nE[{}]: {}".format(i, e[i]))
    print("K[{}]: {}".format(i, k[i]))
    print("A[{}]: {}".format(i, a[i]))
    print("B[{}]: {}".format(i, b[i]))
    print("P(B)[{}]: {}".format(i, p[i]))
    print("L[{}]: {}".format(i, l[i]))
    print("R[{}]: {}".format(i, r[i]))

print("\nFinal L dan R :")
print("L[16] :", r[15])
print("R[16] :", r[16])

rl = r[16] + r[15]
print("R[16]L[16] Adalah : ", rl)

cipher = permute(rl, ip_inverse_permutation_table)
print("Hasil Akhir Adalah : ", cipher)

cipher_hex = binary_to_hex(cipher)
>>>>>>> 2c1d54e52eabb949b258d3a9673fd3da8bda18ef
print("Cipher dalam format heksadesimal:", cipher_hex)