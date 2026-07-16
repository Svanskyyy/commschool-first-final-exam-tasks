import logging

# ლოგერის კონფიგურაცია
logging.basicConfig(
    filename="hotel_bookings.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class Room:
    def __init__(self, room_number: int, room_type: str, price_per_night: float, max_guests: int):
        self.room_number = room_number
        self.room_type = room_type  # Single, Double, Suite
        self.price_per_night = price_per_night
        self.is_available = True
        self.max_guests = max_guests

    def book_room(self):
        self.is_available = False

    def release_room(self):
        self.is_available = True

    def calculate_price(self, nights: int) -> float:
        return self.price_per_night * nights

    def __str__(self):
        status = "თავისუფალი" if self.is_available else "დაკავებული"
        return (f"ოთახი #{self.room_number} ({self.room_type}) | "
                f"ფასი: {self.price_per_night} GEL/ღამე | "
                f"ტევადობა: {self.max_guests} სტუმარი | სტატუსი: {status}")


class Customer:
    def __init__(self, name: str, budget: float):
        self.name = name
        self.budget = budget
        self.booked_rooms = []  # Room ობიექტების სია
        self.reward_points = 0  # ქულების დაგროვების სისტემა

    def add_room(self, room: Room):
        self.booked_rooms.append(room)

    def remove_room(self, room: Room):
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)

    def pay_for_booking(self, total_price: float) -> bool:
        if self.budget >= total_price:
            self.budget -= total_price
            # ბონუს ქულების დარიცხვა: ყოველ დახარჯულ 10 ლარზე 1 ქულა
            earned_points = int(total_price // 10)
            self.reward_points += earned_points
            print(f"გადახდა წარმატებულია! დაგერიცხათ {earned_points} ბონუს ქულა.")
            return True
        return False

    def show_booking_summary(self) -> str:
        if not self.booked_rooms:
            return f"მომხმარებელ {self.name}-ს არ აქვს აქტიური დაჯავშნები."

        rooms_info = ", ".join([f"#{r.room_number}" for r in self.booked_rooms])
        return (f"მომხმარებელი: {self.name} | "
                f"დაჯავშნილი ოთახები: [{rooms_info}] | "
                f"ნაშთი ბიუჯეტზე: {self.budget:.2f} GEL | "
                f"ბონუს ქულები: {self.reward_points}")


class Hotel:
    def __init__(self, name: str):
        self.name = name
        self.rooms = []  # სასტუმროს ყველა ოთახი
        self.bookings_log = []  # ლოგების ისტორია

    def add_room_to_hotel(self, room: Room):
        self.rooms.append(room)

    def show_available_rooms(self, room_type: str = None) -> list:
        available = []
        for r in self.rooms:
            if r.is_available:
                if room_type is None or r.room_type.lower() == room_type.lower():
                    available.append(r)
        return available

    def calculate_total_booking(self, room_number: int, nights: int) -> float:
        for r in self.rooms:
            if r.room_number == room_number:
                return r.calculate_price(nights)
        return 0.0

    def log_booking(self, customer: Customer, room: Room, total_price: float):
        log_entry = (f"დაჯავშნა: მომხმარებელი: {customer.name} | "
                     f"ოთახი #{room.room_number} | "
                     f"ჯამური ფასი: {total_price:.2f} GEL")
        self.bookings_log.append(log_entry)
        logging.info(log_entry)  # იწერება hotel_bookings.log ფაილში

    def book_room_for_customer(self, customer: Customer, room_number: int, nights: int) -> bool:
        for r in self.rooms:
            if r.room_number == room_number:
                if not r.is_available:
                    print("ეს ოთახი უკვე დაკავებულია!")
                    return False

                total_price = r.calculate_price(nights)
                if customer.pay_for_booking(total_price):
                    r.book_room()
                    customer.add_room(r)
                    self.log_booking(customer, r, total_price)
                    print(f"ოთახი #{room_number} წარმატებით დაიჯავშნა {customer.name}-თვის {nights} ღამით!")
                    return True
                else:
                    print("ანგარიშზე არ არის საკმარისი თანხა!")
                    return False
        print("ოთახი ამ ნომრით ვერ მოიძებნა!")
        return False

    def cancel_booking(self, customer: Customer, room_number: int):
        for r in customer.booked_rooms:
            if r.room_number == room_number:
                r.release_room()
                customer.remove_room(r)

                log_entry = f"მომხმარებელმა {customer.name} გააუქმა ოთახი #{room_number}"
                self.bookings_log.append(log_entry)
                logging.info(log_entry)
                print(f"დაჯავშნა ოთახზე #{room_number} წარმატებით გაუქმდა!")
                return
        print("მოცემული ოთახის დაჯავშნა ამ მომხმარებელზე ვერ მოიძებნა!")


# კონსოლის გაშვება
def main():
    hotel = Hotel("Hotel Georgia")

    # ოთახების დამატება
    hotel.add_room_to_hotel(Room(10, "Single", 100.0, 1))
    hotel.add_room_to_hotel(Room(11, "Single", 100.0, 1))
    hotel.add_room_to_hotel(Room(12, "Single", 100.0, 1))
    hotel.add_room_to_hotel(Room(20, "Double", 200.0, 2))
    hotel.add_room_to_hotel(Room(21, "Double", 200.0, 2))
    hotel.add_room_to_hotel(Room(22, "Double", 200.0, 2))
    hotel.add_room_to_hotel(Room(30, "Suite", 300.0, 4))
    hotel.add_room_to_hotel(Room(31, "Suite", 300.0, 4))
    hotel.add_room_to_hotel(Room(32, "Suite", 300.0, 4))

    print("=========================================")
    print("სასტუმროს დაჯავშნის სისტემა")
    print("=========================================")

    # იქმნება მომხმარებელი
    name = input("შეიყვანეთ თქვენი სახელი: ").strip()
    budget = float(input("შეიყვანეთ თქვენი ბიუჯეტი (GEL): "))

    # დინამიური შემოწმება: ვპოულობთ ყველაზე იაფი ოთახის ობიექტს
    if hotel.rooms:
        cheapest_room = min(hotel.rooms, key=lambda r: r.price_per_night)
        if budget < cheapest_room.price_per_night:
            print(f"\nსამწუხაროდ, ჩვენთან საწყისი ფასი {cheapest_room.room_type} ნომერზე იწყება "
                  f"{cheapest_room.price_per_night:.2f} GEL-იდან. "
                  f"თქვენი ბიუჯეტი ({budget:.2f} GEL) არ არის საკმარისი, "
                  f"შესაბამისად თქვენ ვერ შეძლებთ ჩვენთან ჯავშნის გაკეთებას.")
            return  # პროგრამის მუშაობის დასრულება

    customer = Customer(name, budget)

    while True:
        print("\n-----------------------------------------")
        print("ჩამონათვალი:")
        print("1. თავისუფალი ოთახების ნახვა")
        print("2. ოთახის დაჯავშნა")
        print("3. აქტიური ჯავშნების ნახვა")
        print("4. ჯავშანის გაუქმება")
        print("5. პროგრამიდან გამოსვლა")
        print("-----------------------------------------")

        choice = input("აირჩიეთ სასურველი ოპერაცია (1-5): ").strip()

        if choice == "1":
            print("\nფილტრი:")
            print("1. ყველა თავისუფალი ოთახი")
            print("2. ფილტრი ტიპის მიხედვით (Single, Double, Suite)")
            filter_choice = input("აირჩიეთ (1-2): ").strip()

            if filter_choice == "2":
                r_type = input("შეიყვანეთ ტიპი (Single, Double, Suite): ").strip()
                rooms = hotel.show_available_rooms(r_type)
            else:
                rooms = hotel.show_available_rooms()

            if not rooms:
                print("თავისუფალი ოთახები არ არის.")
            else:
                print("\nთავისუფალი ოთახები:")
                for r in rooms:
                    print(r)

        elif choice == "2":
            try:
                r_num = int(input("\nშეიყვანეთ სასურველი ოთახის ნომერი: "))
                nights = int(input("შეიყვანეთ სასურველი ღამეების რაოდენობა: "))
                hotel.book_room_for_customer(customer, r_num, nights)
            except ValueError:
                print("გთხოვთ შეიყვანოთ მხოლოდ რიცხვები!")

        elif choice == "3":
            print(f"\n{customer.show_booking_summary()}")

        elif choice == "4":
            try:
                r_num = int(input("\nშეიყვანეთ გასაუქმებელი ოთახის ნომერი: "))
                hotel.cancel_booking(customer, r_num)
            except ValueError:
                print("გთხოვთ შეიყვანოთ სწორი ოთახის ნომერი!")

        elif choice == "5":
            print("\nგმადლობთ, რომ სარგებლობთ ჩვენი სასტუმროთი! ნახვამდის.")
            break
        else:
            print("არასწორია! გთხოვთ სცადოთ თავიდან.")


if __name__ == "__main__":
    main()