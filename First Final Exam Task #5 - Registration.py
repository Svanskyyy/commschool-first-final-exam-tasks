import string

# წინასწარ შენახული მონაცემები
user_data = {
    "email": "mattmurdock@gmail.com",
    "username": "daredevil",
    "password": "stanlee123"
}

LATIN_LOWERCASE = set(string.ascii_lowercase)

def validate_name(name):
    # 1. სიცარიელის შემოწმება
    if not name:
        return "ველი არ უნდა იყოს ცარიელი, შემოიტანეთ მხოლოდ string პატარა რეგისტრში"

    # 2. რიცხვების შემოწმება
    if name.isdigit():
        return "შემოყვანილია რიცხვითი მნიშვნელობა, შემოიტანეთ მხოლოდ string პატარა რეგისტრში"

    # 3. სიმბოლოების შემოწმება
    has_symbols = any(not char.isalnum() and not char.isspace() for char in name)
    if has_symbols:
        return "შემოყვანილია სიმბოლოები, შემოიტანეთ მხოლოდ string პატარა რეგისტრში"

    # 4. სხვა ენის შემოწმება
    is_latin = all(char in LATIN_LOWERCASE or char.isspace() for char in name)

    # თუ ასოებია, მაგრამ არა ლათინური
    if name.isalpha() and not is_latin:
        # ვამოწმებთ, ხომ არ არის დიდი ასოებიც შერეული სხვა ენაში
        return "შემოყვანილია სხვა ენა, შემოიტანეთ მხოლოდ ლათინური ასოები პატარა რეგისტრში"

    # 5. დიდი ასოების შემოწმება ლათინურისთვის
    if not name.islower() and is_latin:
        return "შემოყვანილია დიდი ასოები, შემოიტანეთ მხოლოდ string პატარა რეგისტრში"

    # თუ ყველა სხვა შემთხვევა გამოირიცხა, მაგრამ მაინც არ არის სუფთა ლათინური პატარა ასოები
    if not is_latin:
        return "შეცდომა: შემოიტანეთ მხოლოდ ლათინური ასოები პატარა რეგისტრში"

    return "valid"


def main():
    print("=" * 50)
    print("რეგისტრაცია")
    print("=" * 50)

    while True:
        name_input = input("გთხოვთ შეიყვანოთ თქვენი სახელი: ").strip()

        validation_result = validate_name(name_input)

        if validation_result == "valid":
            # წარმატებული რეგისტრაცია - ვინახავთ სახელს და გამოგვაქვს მონაცემები
            user_data["name"] = name_input

            print("\n" + "=" * 50)
            print("რეგისტრაცია დასრულებულია!")
            print("=" * 50)
            print(f"სახელი: {user_data['name']}")
            print(f"ელ-ფოსტა: {user_data['email']}")
            print(f"ზედმეტსახელი: {user_data['username']}")
            print(f"პაროლი: {user_data['password']}")
            print("=" * 50)
            break
        else:
            # შეცდომის გამოტანა და თავიდან შეყვანის მოთხოვნა
            print(f"{validation_result}\n")


if __name__ == "__main__":
    main()