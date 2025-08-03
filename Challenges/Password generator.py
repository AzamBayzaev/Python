import random
import string

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_punctuation=True):
    if length < 8:
        print("Длина пароля должна быть не меньше 8. Установлено 8 по умолчанию.")
        length = 8

    char_sets = []
    if use_upper:
        char_sets.append(string.ascii_uppercase)
    if use_lower:
        char_sets.append(string.ascii_lowercase)
    if use_digits:
        char_sets.append(string.digits)
    if use_punctuation:
        char_sets.append(string.punctuation)

    if not char_sets:
        print("Вы должны выбрать хотя бы один тип символов!")
        return ""


    password_list = [random.choice(char_set) for char_set in char_sets]

    all_chars = ''.join(char_sets)
    remaining_length = length - len(password_list)
    password_list += [random.choice(all_chars) for _ in range(remaining_length)]

    random.shuffle(password_list)
    password = ''.join(password_list)
    return password

def password_strength(password):
    length = len(password)
    categories = 0
    if any(c.islower() for c in password):
        categories += 1
    if any(c.isupper() for c in password):
        categories += 1
    if any(c.isdigit() for c in password):
        categories += 1
    if any(c in string.punctuation for c in password):
        categories += 1

    if length >= 12 and categories == 4:
        return "Очень сильный"
    elif length >= 10 and categories >= 3:
        return "Сильный"
    elif length >= 8 and categories >= 2:
        return "Средний"
    else:
        return "Слабый"

def yes_no_input(prompt):
    while True:
        ans = input(prompt + " (д/н): ").strip().lower()
        if ans in ('д', 'да', 'y', 'yes'):
            return True
        elif ans in ('н', 'нет', 'n', 'no'):
            return False
        else:
            print("Пожалуйста, ответьте 'д' или 'н'.")

def main():
    print("Генератор паролей")

    while True:
        length_input = input("Введите желаемую длину пароля (минимум 8, по умолчанию 12): ")
        if length_input == "":
            length = 12
            break
        elif length_input.isdigit() and int(length_input) >= 8:
            length = int(length_input)
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите число 8 или больше.")

    use_upper = yes_no_input("Включать заглавные буквы?")
    use_lower = yes_no_input("Включать строчные буквы?")
    use_digits = yes_no_input("Включать цифры?")
    use_punctuation = yes_no_input("Включать спецсимволы?")

    password = generate_password(length, use_upper, use_lower, use_digits, use_punctuation)
    if password:
        print(f"\nСгенерированный пароль: {password}")
        print(f"Оценка надежности: {password_strength(password)}")

if __name__ == "__main__":
    main()
