from datetime import datetime

# საწყისი ბალანსი
balance = 1000.0
LOG_FILE = "atm_log.txt"


# დამხმარე ფუნქცია ლოგების ფაილში ჩასაწერად
def log_transaction(action, amount):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}] ოპერაცია: {action} | თანხა: {amount} GEL\n"

    # ვიყენებთ "a" (append) რეჟიმს, რომ ახალი ლოგები ბოლოში მიეწეროს
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_message)


# მთავარი ციკლი
while True:
    print("\n" + "=" * 40)
    print("ბანკომატის საწყისი ფანჯარა")
    print("=" * 40)
    print("1. ბალანსის შემოწმება")
    print("2. თანხის შემოტანა")
    print("3. თანხის გატანა")
    print("4. პროგრამიდან გამოსვლა")
    print("=" * 40)

    choice = input("აირჩიეთ სასურველი ოპერაცია (1-4): ").strip()

    if choice == "1":
        # ბალანსის ნახვა
        print(f"\nთქვენს ანგარიშზეა: {balance:.2f} GEL")

    elif choice == "2":
        # თანხის შემოტანა
        amount = float(input("\nშეიყვანეთ შესატანი თანხა: "))

        # ვალიდაცია: ერთჯერადად მაქსიმუმ 1000 ლარი
        if amount > 1000:
            print("შეცდომა: ერთჯერადად 1000 ლარზე მეტის შემოტანა შეუძლებელია!")
        else:
            balance += amount
            print(f"თანხა წარმატებით შემოტანილია. ახალი ბალანსი: {balance:.2f} GEL")
            # ტრანზაქციის ლოგირება
            log_transaction("თანხის შემოტანა", amount)

    elif choice == "3":
        # თანხის გატანა
        amount = float(input("\nშეიყვანეთ გასატანი თანხა: "))

        # ვალიდაცია: არ უნდა გაიტანოს ბალანსზე მეტი
        if amount > balance:
            print(f"შეცდომა: ანგარიშზე არ არის საკმარისი თანხა! მაქსიმუმ შეგიძლიათ გაიტანოთ: {balance:.2f} GEL")
        else:
            balance -= amount
            print(f"თანხა წარმატებით გატანილია. ახალი ბალანსი: {balance:.2f} GEL")
            # ტრანზაქციის ლოგირება
            log_transaction("თანხის გატანა", amount)

    elif choice == "4":
        print("\nგმადლობთ, რომ სარგებლობთ ჩვენი მომსახურებით! ნახვამდის.")
        break
    else:
        print("\nბრძანება არასწორია! გთხოვთ აირჩიოთ 1-დან 4-მდე.")