import unittest
import parameterized
from unittest.mock import Mock
#1
class MathTools:
    @staticmethod
    def add(a, b):
        return a + b
    @staticmethod
    def subtract(a, b):
        return a - b    
    @staticmethod
    def multiply(a, b):
        return a * b
    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
class TestMathTools(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(MathTools.add(10, 5), 15)
        self.assertEqual(MathTools.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(MathTools.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(MathTools.multiply(3, 7), 21)

    def test_divide(self):
        self.assertEqual(MathTools.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            MathTools.divide(10, 0)

if __name__ == '__main__':
    unittest.main()


#2
class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    def details(self):
        return f"{self.title} by {self.author} ({self.year})"
class TestLibraryItem(unittest.TestCase):
    def test_details(self):
        item = LibraryItem("1984", "George Orwell", 1949)
        self.assertEqual(item.details(), "1984 by George Orwell (1949)")
        item2 = LibraryItem("The Midnight Library", "Matt Haig", 2020)
        self.assertEqual(item2.details(), "The Midnight Library by Matt Haig (2020)")

    def test_attributes(self):
        item = LibraryItem("Kobzar", "Taras Shevchenko", 1840)
        self.assertEqual(item.title, "Kobzar")
        self.assertEqual(item.author, "Taras Shevchenko")
        self.assertEqual(item.year, 1840)
if __name__ == '__main__':   
    unittest.main()

#3
class NotificationService:
    def send_email(self, recipient, subject, message):
        
        return f"Email sent to {recipient}"

    def send_sms(self, recipient, message):
        return f"SMS sent to {recipient}"

class UserManager:
    def __init__(self, notification_service):
        self.notification_service = notification_service

    def notify_user(self, user_email, message):
        return self.notification_service.send_email(user_email, "Notification", message)

class TestUserManager(unittest.TestCase):
    def test_notify_user_calls_send_email(self):
       
        mock_service = Mock(spec=NotificationService)
        user_manager = UserManager(mock_service)
        
        email = "test@example.com"
        msg = "Hello World"
        user_manager.notify_user(email, msg)
        
        mock_service.send_email.assert_called_with(email, "Notification", msg)
        
        self.assertEqual(mock_service.send_email.call_count, 1)

if __name__ == '__main__':
    unittest.main()

#4
class Number:
    def check_even(self, num):
        if num % 2 == 0:
            return "true"
        else:
            return "false"
@parameterized.parameterized.expand([
    (2, "true"),
    (3, "false"),
    (0, "true"),
    (-4, "true"),
    (-5, "false")
])
def test_check_even(self, name, num, expected):
        self.assertEqual(self.calc.check_even(num), expected)

if __name__ == '__main__':
    unittest.main()