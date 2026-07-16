import random
from datetime import datetime

# საწყისი პარამეტრები
JACKPOT = 5200000.0
LOG_FILE = "lottery_log.txt"


# დამხმარე ფუნქცია ლოგების ფაილში ჩასაწერად
def log_game(user_numbers, winning_numbers, matches, win_amount):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = (
        f"[{current_time}] მოთამაშის რიცხვები: {user_numbers} | "
        f"მომგებიანი რიცხვები: {winning_numbers} | "
        f"დამთხვევა: {matches} | "
        f"მოგებული თანხა: {win_amount:,.2f} GEL\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_message)


def play_lottery():
    print("=" * 50)
    print("ლატარიის სიმულატორი 6/49")
    print("=" * 50)

    # 1. კომპიუტერი ირჩევს 6 შემთხვევით უნიკალურ რიცხვს 1-დან 49-მდე
    winning_numbers = sorted(random.sample(range(1, 50), 6))

    # 2. მოთამაშეს შეჰყავს 6 რიცხვი
    user_numbers = []
    print("გთხოვთ, შეიყვანოთ 6 განსხვავებული რიცხვი (1-დან 49-მდე):")
    while len(user_numbers) < 6:
        num = int(input(f"შეიყვანეთ მე-{len(user_numbers) + 1} რიცხვი: "))

        # უსაფრთხოების მიზნით ვამოწმებთ დიაპაზონს და დუბლიკატებს
        if num < 1 or num > 49:
            print("შეცდომა: რიცხვი უნდა იყოს 1-დან 49-მდე!")
        elif num in user_numbers:
            print("შეცდომა: ეს რიცხვი უკვე შეყვანილი გაქვთ!")
        else:
            user_numbers.append(num)

    user_numbers.sort()

    # 3. დამთხვევების დათვლა სიმრავლეების (Sets) მეშვეობით
    user_set = set(user_numbers)
    winning_set = set(winning_numbers)
    matching_numbers = user_set.intersection(winning_set)
    matches_count = len(matching_numbers)

    # 4. მოგებული თანხის გამოთვლა
    win_amount = 0.0
    result_text = ""

    if matches_count == 6:
        win_amount = JACKPOT
        result_text = "გილოცავთ! თქვენ მოიგეთ JACKPOT!"
    elif matches_count == 5:
        # 5 დამთხვევა: ჯეკპოტს აკლდება 40%
        win_amount = JACKPOT * 0.60
        result_text = "გილოცავთ! თქვენ დაამთხვიეთ 5 რიცხვი"
    elif matches_count == 4:
        # 4 დამთხვევა: ჯეკპოტს აკლდება 60%
        win_amount = JACKPOT * 0.40
        result_text = "გილოცავთ! თქვენ დაამთხვიეთ 4 რიცხვი"
    elif matches_count == 3:
        # 3 დამთხვევა: ჯეკპოტს აკლდება 80%
        win_amount = JACKPOT * 0.20
        result_text = "გილოცავთ! თქვენ დაამთხვიეთ 3 რიცხვი"
    else:
        # 2 ან 1 დამთხვევის შემთხვევაში მოგება არის 0
        win_amount = 0.0
        result_text = "სამწუხაროდ, თქვენ ვერაფერი მოიგეთ"

    # 5. შედეგების ეკრანზე გამოტანა
    print("\n" + "-" * 50)
    print(f"თქვენი რიცხვები: {user_numbers}")
    print(f"მომგებიანი რიცხვები: {winning_numbers}")
    print(f"დამთხვეული რიცხვები ({matches_count}): {list(matching_numbers)}")
    print("-" * 50)
    print(result_text)
    print(f"მოგებული თანხა: {win_amount:,.2f} GEL")
    print("-" * 50)

    # 6. გათამაშების ლოგირება ფაილში
    log_game(user_numbers, winning_numbers, matches_count, win_amount)


# პროგრამის გაშვება
def main():
    while True:
        play_lottery()
        play_again = input("\nგსურთ კიდევ ერთხელ თამაში? (yes/no): ").strip().lower()
        if play_again != "yes":
            print("\nგმადლობთ რომ ჩვენთან ითამაშეთ! ნახვამდის.")
            break


if __name__ == "__main__":
    main()