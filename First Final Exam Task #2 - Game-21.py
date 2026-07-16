import random

# 1. ფუნქცია, რომელიც ქმნის 52 კარტიან ახალ დასტას
def create_deck():
    suits = ["ყვავი", "ჯვარი", "გული", "აგური"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank} {suit}")

    random.shuffle(deck)  # ასაჩეხად ვიყენებთ random მოდულს
    return deck


# 2. ფუნქცია, რომელიც ითვლის ხელში არსებული კარტების საერთო ქულას
def calculate_score(hand):
    score = 0
    for card in hand:
        # ვიღებთ მხოლოდ კარტის მნიშვნელობას
        rank = card.split()[0]

        if rank in ["Jack", "Queen", "King"]:
            score += 10
        elif rank == "Ace":
            score += 11
        else:
            score += int(rank)

    return score


# 3. თამაშის მთავარი ლოგიკა
def play_round():
    deck = create_deck()

    # საწყისი 2-2 კარტის დარიგება
    player_hand = [deck.pop(), deck.pop()]
    computer_hand = [deck.pop(), deck.pop()]

    # მოთამაშის ჯერი
    while True:
        player_score = calculate_score(player_hand)
        print(f"\nთქვენი კარტები: {player_hand}")
        print(f"თქვენი ქულა: {player_score}")

        # თუ მოთამაშეს საწყის ეტაპზევე აქვს 21-ზე მეტი
        if player_score > 21:
            print("თქვენ გადააჭარბეთ 21 ქულას!")
            break

        action = input("აირჩიეთ მოქმედება ('add' - დამატება, 'stop' - გაჩერება): ").strip().lower()

        if action == "add":
            player_hand.append(deck.pop())
        elif action == "stop":
            break
        else:
            print("არასწორი ბრძანება! ჩაწერეთ მხოლოდ 'add' ან 'stop'.")

    player_score = calculate_score(player_hand)

    # თუ მოთამაშემ გადააჭარბა 21-ს, ის ავტომატურად აგებს
    if player_score > 21:
        print("\nთქვენ წააგეთ! (კომპიუტერი იგებს)")
        return "lose"

    # კომპიუტერის ჯერი
    # კომპიუტერი იღებს კარტებს მანამ, სანამ ქულა < 17
    print("\nკომპიუტერის ჯერია")
    while calculate_score(computer_hand) < 17:
        computer_hand.append(deck.pop())

    computer_score = calculate_score(computer_hand)
    print(f"კომპიუტერის კარტები: {computer_hand}")
    print(f"კომპიუტერის ქულა: {computer_score}")

    # გამარჯვებულის გამოვლენა
    if computer_score > 21:
        print("\nკომპიუტერმა გადააჭარბა 21 ქულას. თქვენ მოიგეთ!")
        return "win"
    elif player_score > computer_score:
        print("\nთქვენ მოიგეთ!")
        return "win"
    elif computer_score > player_score:
        print("\nთქვენ წააგეთ!")
        return "lose"
    else:
        print("\nფრეა!")
        return "draw"


# 4. პროგრამის გაშვების მთავარი ციკლი
def main():
    print("=" * 40)
    print(" კეთილი იყოს თქვენი მობრძანება თამაშში '21'!")
    print("=" * 40)

    while True:
        result = play_round()

        # თუ ფრეა, ვეკითხებით მომხმარებელს სურს თუ არა ხელახლა დარიგება
        if result == "draw":
            choice = input("\nფრეა! გსურთ ხელახლა ვითამაშოთ? (yes/no): ").strip().lower()
            if choice == "yes":
                print("\n--- ვიწყებთ ახალ ხელს! ---")
                continue
            else:
                print("\nმადლობა თამაშისთვის! ნახვამდის.")
                break
        else:
            # თუ ვინმემ მოიგო ან წააგო, ვეკითხებით სურს თუ არა თავიდან დაწყება
            play_again = input("\nგსურთ კიდევ ერთი ხელი? (yes/no): ").strip().lower()
            if play_again != "yes":
                print("\nმადლობა თამაშისთვის! ნახვამდის.")
                break
            print("\n" + "=" * 40 + "\n ახალი თამაში იწყება!")


# პროგრამის გაშვება
if __name__ == "__main__":
    main()