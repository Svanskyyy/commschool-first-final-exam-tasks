import unittest
import importlib.util
import os
import sys

file_name = "First Final Exam Task #6.1 - Hotel.py"

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, file_name)

if not os.path.exists(file_path):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)

if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"\nშეცდომა: ფაილი სახელით '{file_name}' ვერ მოიძებნა!\n"
        f"დარწმუნდით, რომ 'test_hotel.py' და '{file_name}' ერთსა და იმავე საქაღალდეშია."
    )

# იმპორტი
spec = importlib.util.spec_from_file_location("hotel_module", file_path)
hotel_module = importlib.util.module_from_spec(spec)
sys.modules["hotel_module"] = hotel_module
spec.loader.exec_module(hotel_module)

Room = hotel_module.Room
Customer = hotel_module.Customer
Hotel = hotel_module.Hotel


class TestHotelBookingSystem(unittest.TestCase):

    def setUp(self):
        self.hotel = Hotel("Test Hotel")
        self.room = Room(10, "Single", 100.0, 1)
        self.hotel.add_room_to_hotel(self.room)
        self.customer = Customer("Levani", 200.0)

    # 1. ტესტი ბიუჯეტის შემცირებაზე
    def test_pay_for_booking_reduces_budget(self):
        initial_budget = self.customer.budget
        payment_amount = 100.0

        success = self.customer.pay_for_booking(payment_amount)

        self.assertTrue(success)
        self.assertEqual(self.customer.budget, initial_budget - payment_amount)
        self.assertEqual(self.customer.reward_points, 10)

    # 2. ტესტი არასაკმარისი ბიუჯეტის შემთხვევაში
    def test_pay_for_booking_fails_insufficient_budget(self):
        success = self.customer.pay_for_booking(300.0)
        self.assertFalse(success)
        self.assertEqual(self.customer.budget, 200.0)

    # 3. ტესტი თავისუფალი ოთახის დაჯავშნაზე
    def test_book_available_room_success(self):
        success = self.hotel.book_room_for_customer(self.customer, 10, 2)

        self.assertTrue(success)
        self.assertFalse(self.room.is_available)
        self.assertIn(self.room, self.customer.booked_rooms)

    # 4. ტესტი უკვე დაკავებული ოთახის დაჯავშნაზე
    def test_book_already_booked_room_fails(self):
        self.room.book_room()
        success = self.hotel.book_room_for_customer(self.customer, 10, 2)

        self.assertFalse(success)
        self.assertNotIn(self.room, self.customer.booked_rooms)


if __name__ == "__main__":
    unittest.main()