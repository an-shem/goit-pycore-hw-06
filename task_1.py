from collections import UserDict
from error import (
    ContactNotFoundError,
    DuplicatePhoneNumberError,
    InvalidContactError,
    InvalidNumberError,
    PhoneNumberNotFoundError,
)


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        if type(name) != str:
            raise InvalidContactError(f"Name must be a string")
        name = name.strip()
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        phone = phone.strip()
        if len(phone) != 10:
            raise InvalidNumberError(
                f"The number '{phone}' is invalid! It must be 10 characters long."
            )
        super().__init__(phone)


class Record:
    def __init__(self, name: str):
        try:
            self.name = Name(name)
        except InvalidContactError:
            raise
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        try:
            ph = Phone(phone)
            for p in self.phones:
                if p.value == phone:
                    raise DuplicatePhoneNumberError(
                        f"Contact {self.name} already has the telephone number {phone}."
                    )
            self.phones.append(ph)
        except (InvalidNumberError, DuplicatePhoneNumberError):
            raise
        except Exception:
            raise

    def edit_phone(self, old_phone, new_phone):
        if not old_phone or not new_phone or old_phone == new_phone:
            raise InvalidNumberError("Phone numbers entered incorrectly.")
        [index] = [i for i, p in enumerate(self.phones) if p.value == old_phone]
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        if not phone:
            raise InvalidNumberError("Phone numbers entered incorrectly.")
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise PhoneNumberNotFoundError("Phone number not found.")

    def remove_phone(self, phone):
        if not phone or len(phone) != 10:
            raise InvalidNumberError("Phone numbers entered incorrectly.")
        [index] = [i for i, p in enumerate(self.phones) if p.value == phone]
        del self.phones[index]
        return phone


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not isinstance(record, Record):
            raise ValueError(
                "In AddressBook, you can append only an object of the Record class."
            )
        name_key = record.name.value
        if not name_key:
            raise ValueError("You cannot add a contact without a name to AddressBook.")
        if name_key in self.data:
            raise DuplicatePhoneNumberError("Contact with that name already exists.")
        self.data[name_key] = record
        return self.data[name_key]

    def find(self, name):
        if not name in self.data:
            raise ContactNotFoundError("Contact with this name not found.")
        return self.data[name]

    def delete(self, name):
        if not name:
            raise InvalidContactError("Name entered incorrectly.")
        if name in self.data:
            contact = self.data[name]
            del self.data[name]
            return contact


def main():
    try:
        # Створення нової адресної книги
        book = AddressBook()
        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        # # Додавання запису John до адресної книги
        book.add_record(john_record)
        # # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)
        # # Виведення всіх записів у книзі
        for name, record in book.data.items():
            print(record)
        # # Знаходження та редагування телефону для John
        john = book.find("John")
        john.edit_phone("1234567890", "1112223333")
        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
        # # Пошук конкретного телефону в записі John
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
        # # Видалення запису Jane
        book.delete("Jane")
        john.remove_phone("1112223333")

        for _, record in book.data.items():
            print(record)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
