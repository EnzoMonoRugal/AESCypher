# -*- coding: utf-8 -*-
"""CifraAES.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ne6nmaoVVUVZoKJRBTOxcCiwlmVEVj1w
"""

from enum import Enum

# Definindo os códigos de erro
class ErrorCode(Enum):
    SUCCESS = 0
    ERROR_AES_UNKNOWN_KEYSIZE = 1
    ERROR_MEMORY_ALLOCATION_FAILED = 2


# Definindo tamanhos de chave
class KeySize(Enum):
    SIZE_16 = 16
    SIZE_24 = 24
    SIZE_32 = 32

sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]


Rcon = [
    0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
    0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab,
    0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
    0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25,
    0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
    0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
    0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa,
    0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
    0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02,
    0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
    0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb]

def main():
    # Definições de tamanho da chave expandida e do bloco
    expandedKeySize = 176# Tamanho da chave expandida em bytes
    size = 16 # Tamanho do bloco em bytes

    # Inicializando variáveis
    expandedKey = bytearray(expandedKeySize)# Chave expandida
    key = bytearray(16)# Chave original
    plaintext = bytearray(16) # Texto plano
    ciphertext = bytearray(16)  # Texto cifrado

    # Chave e texto plano em formato HEX
    hex_key = "0f2571c947d9e8590cb7add6af7f6798"
    hex_plain_text = "0123456789abcdeffedcba9876543210"

    # Converter chave e plaintext de hexadecimal para bytes
    hexStringToBytes(hex_key, key, 16)
    hexStringToBytes(hex_plain_text, plaintext, 16)

    # Expandir a chave /Criptografar o texto plano
    expandKey(expandedKey, key, size, expandedKeySize)
    aes_encrypt(plaintext, ciphertext, key, 16)

   # Exibir o texto cifrado em formato HEX
    print("\nTexto cifrado (HEX):")
    for i in range(16):
        print(f"{ciphertext[i]:02x}", end="")
    print()

# Converter cada par de caracteres HEX para byte
def hexStringToBytes(hexString, byteArray, byteArraySize):
    for i in range(byteArraySize):
        byteArray[i] = int(hexString[2 * i:2 * i + 2], 16)

def getSBoxValue(num):
    return sbox[num] # Retorna o valor da SBox

def rotate(word):# Rotaciona os bytes de uma palavra
    c = word[0]
    for i in range(3):
        word[i] = word[i + 1]
    word[3] = c

def getRconValue(num):# Retorna o valor de Rcon
    return R_CON[num]

def core(word, iteration):
    rotate(word)# Rotaciona a palavra
    for i in range(4):
        word[i] = getSBoxValue(word[i])# Aplica a SBox
    word[0] = word[0] ^ getRconValue(iteration)# XOR com Rcon

def expandKey(expandedKey, key, size, expandedKeySize):
    currentSize = 0 # Inicializa o tamanho atual da chave expandida
    rconIteration = 1 # Inicializa um contador que usando para a RCON durante a expansão da chave
    t = bytearray(4) # array que sera utilizado para armazenar temporariamente a chave espandida

    for i in range(size):# Copiar a chave original para a chave expandida
        expandedKey[i] = key[i]
    currentSize += size

    while currentSize < expandedKeySize: # Expandir a chave até atingir o tamanho desejado
        for i in range(4):
            t[i] = expandedKey[currentSize - 4 + i]# Última palavra da chave expandida

        if currentSize % size == 0:
            core(t, rconIteration) # Aplica a função core
            rconIteration += 1

        if size == 32 and (currentSize % size) == 16:
            for i in range(4):
                t[i] = getSBoxValue(t[i])# Aplica SBox
        for i in range(4):
            expandedKey[currentSize] = expandedKey[currentSize - size] ^ t[i]# XOR com a palavra anterior
            currentSize += 1

def subBytes(state):
    for i in range(16):
        state[i] = getSBoxValue(state[i])# Substitui bytes usando a SBox

def shiftRows(state):
    for i in range(4):
        shiftRow(state, i * 4, i)# Aplica a função shiftRow para cada linha

def shiftRow(state, start, nbr):
    for _ in range(nbr):
        tmp = state[start]# Armazena o primeiro byte
        for j in range(3):
            state[start + j] = state[start + j + 1]# Desloca bytes
        state[start + 3] = tmp# Coloca o primeiro byte no final

def addRoundKey(state, roundKey):
    for i in range(16):
        state[i] = state[i] ^ roundKey[i]# Aplica a chave da rodada

def galois_multiplication(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a# Se o bit menos significativo de b é 1, aplica XOR
        hi_bit_set = a & 0x80# Verifica se o bit mais significativo de a está definido
        a <<= 1 # Multiplica a por 2
        if hi_bit_set:
            a ^= 0x1b  # Reduz a 0x1b (polinômio irreducível)
        b >>= 1 # Divide b por 2
    return p % 256  # Garantir que o resultado esteja dentro do intervalo de bytes

def mixColumns(state):
    for i in range(4):
        column = [state[j * 4 + i] for j in range(4)]# Extrai a coluna, verificar se cada valor está dentro do intervalo
        mixColumn(column)# Aplica a função mixColumn
        for value in column:
            assert 0 <= value < 256, f"Valor fora do intervalo: {value}"
        for j in range(4):
            state[j * 4 + i] = column[j]# Reinsere a coluna



def mixColumn(column):
    cpy = column[:]# Copia a coluna original
     # Aplica as operações de Galois para misturar os valores
    column[0] = galois_multiplication(cpy[0], 2) ^ galois_multiplication(cpy[3], 1) ^ galois_multiplication(cpy[2], 1) ^ galois_multiplication(cpy[1], 3)
    column[1] = galois_multiplication(cpy[1], 2) ^ galois_multiplication(cpy[0], 1) ^ galois_multiplication(cpy[3], 1) ^ galois_multiplication(cpy[2], 3)
    column[2] = galois_multiplication(cpy[2], 2) ^ galois_multiplication(cpy[1], 1) ^ galois_multiplication(cpy[0], 1) ^ galois_multiplication(cpy[3], 3)
    column[3] = galois_multiplication(cpy[3], 2) ^ galois_multiplication(cpy[2], 1) ^ galois_multiplication(cpy[1], 1) ^ galois_multiplication(cpy[0], 3)

def aes_round(state, roundKey):
    print("\nChave da rodada:")
    for i in range(16):
        print(f"{state[i]:02x}", end=" " if (i + 1) % 4 else "\n")

    print("\nEstado inicial:")
    for i in range(16):
        print(f"{state[i]:02x}", end=" " if (i + 1) % 4 else "\n")

    subBytes(state)# Aplica a substituição de bytes
    print("\nApós SubBytes:")
    for i in range(16):
        print(f"{state[i]:02x}", end=" " if (i + 1) % 4 else "\n")

    shiftRows(state)# Aplica o deslocamento das linhas
    print("\nApós ShiftRows:")
    for i in range(16):
        print(f"{state[i]:02x}", end=" " if (i + 1) % 4 else "\n")

    mixColumns(state)# Mistura as colunas
    print("\nApós MixColumns:")
    for i in range(16):
        print(f"{state[i]:02x}", end=" " if (i + 1) % 4 else "\n")

    addRoundKey(state, roundKey)
    print("\nApós a RoundKey:")# Aplica a chave da rodada
    for i in range(16):
        print(f"{state[i]:02x}", end=" " if (i + 1) % 4 else "\n")

def createRoundKey(expandedKey, roundKey):
    for i in range(4):#cria a chave da rodada a partir da chave espandida
        for j in range(4):
            roundKey[i + (j * 4)] = expandedKey[(i * 4) + j]

def aes_main(state, expandedKey, nbrRounds):
    roundKey = bytearray(16)# Inicializa a chave da rodada como um array de bytes de 16 bytes

    # Cria a chave da primeira rodada a partir da chave expandida
    createRoundKey(expandedKey, roundKey)
    addRoundKey(state, roundKey)# Aplica a primeira chave de rodada ao estado

    for i in range(1, nbrRounds):# Loop para executar as rodadas intermediárias
        print(f"\nRound {i}")# Exibe o número da rodada atual
        createRoundKey(expandedKey[16 * i:], roundKey)  # Cria a chave da rodada atual a partir da chave expandida
        aes_round(state, roundKey)# Executa a função de criptografia para a rodada atual
        print(f"\nEnd Round {i}")#fim da rodada

    # Última rodada (sem MixColumns)
    createRoundKey(expandedKey[16 * nbrRounds:], roundKey)# Cria a chave da última rodada
    subBytes(state)# Aplica a substituição de bytes
    shiftRows(state)# Aplica o deslocamento das linhas
    addRoundKey(state, roundKey)# Aplica a última chave de rodada ao estado

def aes_encrypt_hex(hexInput, hexKey, output, size):
   # Inicializa um array de bytes de 16 bytes para os dados de entrada
    input_bytes = bytearray(16)
    # Inicializa um array de bytes para a chave, com tamanho máximo de 32 bytes
    key_bytes = bytearray(32)

  # Converte a string hexadecimal de entrada em bytes
    hexStringToBytes(hexInput, input_bytes, 16)
    # Converte a string hexadecimal da chave em bytes, usando o tamanho especificado
    hexStringToBytes(hexKey, key_bytes, size)
 # Chama a função de criptografia AES e retorna o resultado
    return aes_encrypt(input_bytes, output, key_bytes, size)

def aes_encrypt(input_bytes, output, key, size):
   # Define o número de rodadas baseado no tamanho da chave
    if size == 16:
        nbrRounds = 10# AES-128
    elif size == 24:
        nbrRounds = 12 # AES-192
    elif size == 32:
        nbrRounds = 14# AES-256
    else:
        return ErrorCode.ERROR_AES_UNKNOWN_KEYSIZE # Retorna erro se o tamanho da chave for inválido

    # Calcula o tamanho da chave expandida
    expandedKeySize = (16 * (nbrRounds + 1))
    expandedKey = bytearray(expandedKeySize)# Array para a chave expandida
    block = bytearray(16)# Array para o bloco de entrada
    # Verifica se a alocação de memória para a chave expandida funcionou
    if not expandedKey:
        return ErrorCode.ERROR_MEMORY_ALLOCATION_FAILED

    # Copia os dados de input_bytes para o bloco, transpondo os dados
    for i in range(4):
        for j in range(4):
            block[i + (j * 4)] = input_bytes[i * 4 + j]
    # Expande a chave usando a função expandKey
    expandKey(expandedKey, key, size, expandedKeySize)
    # Executa o processo de criptografia AES no bloco
    aes_main(block, expandedKey, nbrRounds)
    # Transfere o bloco criptografado de volta para o array de saída
    for i in range(4):
        for j in range(4):
            output[i * 4 + j] = block[i + (j * 4)]

    return ErrorCode.SUCCESS# Retorna sucesso após a criptografia

main()