# Module 8 Homework
# This is program for a Command Line Interface bot that allows to interact with an Address Book.
# It allows to add, change, and retrieve a contact's phone number and birthday, view all contacts, or
# a list of contacts with birthdays in the next 7 days
# This module defines the logic.

from cli_ab import *
from datetime import datetime, timedelta
import pickle
from colorama import Fore


def load_data(filename="addressbook.pkl"):  # Load existing or create a new Address Book
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # return new book if file not found


def save_data(book, filename="addressbook.pkl"):  # save Address Book
    with open(filename, "wb") as f:
        pickle.dump(book, f)
    return "Address Book saved."


def input_error(func):  # Decorator function for error handling
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func.__name__ == 'create_contact':
                return "Error creating a contact."
            if func.__name__ == 'delete_contact':
                return "Contact not found in the Address Book."
            if func.__name__ == 'phone':
                return "No such contact or the contact has no phone."
            if func.__name__ == 'show_all':
                return "There are no contacts in the Address Book."
            if func.__name__ == 'change_contact':
                return "There is no such contact."
            if func.__name__ == 'show_birthday':
                return "No birthday for this contact or no such contact."
            return "Incorrect command or attribute"
        except IndexError:
            return "Please enter a command with correct argument(s)."
    return inner


@input_error
def parse_input(user_input):  # Parse user input
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def create_contact(name, book: AddressBook):  # Add name to Address Book
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        print("Contact created.")
    return record


@input_error
def add_phone(args, book: AddressBook):     # Add phone to name record
    name = args[0].title()
    phone_ = args[1]
    record = book.find(name)
    if record is None:
        record = create_contact(name, book)
    message = "Phone number added."
    if phone_:
        record.add_phone(phone_)
    return message


@input_error
def add_birthday(args, book: AddressBook):  # Add birthday to contact
    name = args[0].title()
    birthday = args[1]
    record = book.find(name)
    if record is None:
        record = create_contact(name, book)
    message = "Birthday added/updated."
    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def birthdays(args, book: AddressBook):  # Output congratulations for the next 7 days
    today = datetime.today().date()
    congrats_dict = {}
    for name, birthday in book.items():
        record = book.find(name)
        if record.birthday is None:
            continue
        if birthday.congrats_date() <= today + timedelta(days=7):
                congrats_day = birthday.congrats_date()
                congrats_dict[name] = congrats_day

    # Sort by congratulations date
    congrats_dict_sorted = sorted(congrats_dict.items(), key=lambda x: x[1])

    # Print the sorted congratulations dates, names, and corresponding birthdays
    congrats_header = (f'\nUpcoming birthdays in the next 7 days:\n{"Contact name":20}{"Birthday":23}'
                       f'Congratulations day\n{"-" * 63}\n')
    congrats = f"\n".join(f"{name:20}{str(book[name].birthday):23}"
                          f"{str(congrats_day.strftime('%d.%m.%Y'))}" for name, congrats_day in congrats_dict_sorted)
    # congrats_header = "\nUpcoming birthdays in the next 7 days:\n"
    # congrats = f"\n".join(f"Contact: {name}, \tbirthday: {book[name].birthday}, \tcongratulations date: "
    #                       f"{congrats_day.strftime('%d.%m.%Y')}" for name, congrats_day in congrats_dict_sorted)
    if not congrats:
        congrats = "No upcoming birthdays\n"
    return congrats_header + congrats + '\n'


@input_error
def change_contact(args, book: AddressBook):
    name = args[0].title()
    old_phone = args[1]
    new_phone = args[2]
    if not book.find(name):
        raise ValueError
    rec = book.find(name)
    rec.edit_phone(old_phone, new_phone)
    return "Phone number updated."


@input_error
def delete_contact(args, book: AddressBook):
    name = args[0].title()
    while True:
        user_input = input(f"{Fore.RED}Are you sure?{Fore.RESET} Please enter 'y' or 'n' to confirm: ")
        if user_input in ['N', 'n', 'No', 'no']:
            return "Contact was not deleted."
            break
        elif user_input in ['Y', 'y', 'Yes', 'yes']:
            if not book.find(name):
                raise ValueError
            book.delete(name)
            return "Contact deleted."
        else:
            print("Invalid response. Please enter 'y' or 'n': ")



@input_error
def hello(args, book: AddressBook):
    return "How can I help you?"


commands = {
    "add [Name] [Number]": "add a name with number to Address Book, for example: add Alex 0111222333",
    "add-birthday [Name] [DD.MM.YYYY]": "add or update birthday for contact. If contact doesn't exit, it "
                                        "creates a new one, for example: add-birthday Alex 21.03.2024",
    "all": "display all records in contacts",
    "birthdays": "display contacts with birthdays in the next 7 days",
    "close": "exit the program and save changes",
    "change [Name] [Old Number] [New Number]": "change the phone number for a contact, for example: "
                                               "change Alex 0111222333 0222333444",
    "exit": "exit the program and save changes",
    "hello": "greet the bot",
    "phone [Name]": "display the phone number for a contact, for example: phone Alex",
    "quit": "exit without saving changes",
    "save": "save changes",
    "show-birthday [Name]": "display the birthday for a contact, for example: show-birthday Alex"
}


def help(args, book: AddressBook):
    help_header = "\nThe bot accepts the following commands:\n"
    help_text = f"\n".join(f"{Fore.BLUE} {key:40} {Fore.RESET} {value}" for key, value in commands.items())
    return help_header + help_text + "\n"


@input_error
def phone(args, book: AddressBook):  # Return the phone number(s) for a contact
    name = args[0].title()
    record = book.find(name)
    if not record.phones:
        raise ValueError
    phone_header = f'\n{"Contact name":20}{"Phone number(s)":28}\n{"-" * 43}\n'
    phone_ = f"{str(record.name):20}{', '.join(str(p) for p in record.phones):28}"
    # phone_ = f"Contact name: {record.name}, phone number(s): {', '.join(str(p) for p in record.phones)}"
    return phone_header + phone_ + '\n'


@input_error
def show_birthday(args, book: AddressBook):  # Return birthday for a contact
    name = args[0].title()
    record = book.find(name)
    if record.birthday is None:
        raise ValueError
    birthday_header = f'\n{"Contact name":20}{"Birthday":28}\n{"-" * 31}\n'
    birthday = f"{str(record.name):20}{str(record.birthday):28}"
    # birthday = f"Contact name: {record.name}, birthday: {record.birthday}"
    return birthday_header + birthday + '\n'


@input_error
def show_all(args, book: AddressBook):  # Return all records from Address Book
    if not book:
        raise ValueError
    return book


functions = {
    "add": add_phone,
    "add-bd": add_birthday,
    "add-birthday": add_birthday,
    "all": show_all,
    "bd": birthdays,
    "birthdays": birthdays,
    "change": change_contact,
    "delete": delete_contact,
    "hello": hello,
    "help": help,
    "hi": hello,
    "phone": phone,
    "show-bd": show_birthday,
    "show-birthday": show_birthday,
}


def main():
    book = load_data()
    # book = AddressBook()
    print("Welcome to the assistant bot!")
    print(f"For a list of commands type {Fore.BLUE}help{Fore.RESET}")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        if command == "quit":
            print("Good bye. Changes were not saved!")
            break
        elif command == "save":
            print(save_data(book))
        elif command in functions:
            print(functions[command](args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
