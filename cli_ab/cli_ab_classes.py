# Module 7 Homework
# THis module defines the classes and methods used in the Address Book CLI Bot.

from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.value = value

    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def is_valid(self, value):
        return bool(datetime.strptime(value, "%d.%m.%Y"))

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __str__(self):
        return str(self.value)


class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()


class Record:
    def __init__(self, value):
        self.name = Name(value)
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        birthday = Birthday(value)
        self.birthday = birthday
        return birthday

    def congrats_date(self):  # method returns congratulations date for the record
        today = datetime.today().date()
        birthday = datetime.strptime(str(self.birthday), "%d.%m.%Y").date()

        # Calculate the next birthday
        if datetime(today.year, birthday.month, birthday.day).date() < today:
            next_birthday = (datetime(today.year + 1, birthday.month, birthday.day)).date()
        else:
            next_birthday = datetime(today.year, birthday.month, birthday.day).date()

        # Calculate the congratulations date
        if next_birthday.isoweekday() in [6, 7]:
            congrats_date = next_birthday + timedelta(days=(8 - next_birthday.isoweekday()))
        else:
            congrats_date = next_birthday

        return congrats_date

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)
        return phone

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone

    def remove_phone(self, value):
        phone = self.find_phone(value)
        if not phone:
            raise ValueError
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if not phone:
            raise ValueError
        self.add_phone(new_phone)
        self.remove_phone(old_phone)

    def __str__(self):
        return (f"Contact name: {str(self.name)}, phone(s): {', '.join(str(p) for p in self.phones)}, "
                f"birthday: {str(self.birthday)} ")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

#
# # Створення нової адресної книги
# book = AddressBook()
#
# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# john_record.add_birthday("01.01.2000")
# print("Congrats date:", john_record.congrats_date())
# # Додавання запису John до адресної книги
# book.add_record(john_record)
# print("book: ", book)
#
# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_birthday("01.01.2000")
# jane_record.congrats_date()
# book.add_record(jane_record)
#
# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)
#
# # Знаходження та редагування телефону для John
# john = book.find("John")
# print(john)
# john.edit_phone("1234567890", "1112223333")
#
# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
#
# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
#
# # Видалення запису Jane
# book.delete("Jane")


