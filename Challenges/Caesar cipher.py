def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
          
            result += chr((ord(char) - base + shift) % 26 + base)
        else:

            result += char
    return result

def caesar_decrypt(text, shift):

    return caesar_encrypt(text, -shift)

if __name__ == "__main__":
    message = input("Введите сообщение: ")
    shift = int(input("Введите сдвиг (число): "))

    encrypted = caesar_encrypt(message, shift)
    print("Зашифрованное сообщение:", encrypted)

    decrypted = caesar_decrypt(encrypted, shift)
    print("Расшифрованное сообщение:", decrypted)
