from collections import UserDict


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        phone = phone.strip()
        if len(phone) != 10:
            print("The phone number must consist of 10 digits.")
            return
        for p in self.phones:
            if p.value == phone:
                print(f"Contact {self.name} already has the telephone number {phone}.")
                return
        self.phones.append(Phone(phone))
        print(f"The phone number {phone} has been added to the contact {self.name}.")

    def edit_phone(self, old_phone, new_phone):
        if not old_phone or not new_phone or old_phone == new_phone:
            print("Phone numbers entered incorrectly.")
            return 1
        [index] = [i for i, p in enumerate(self.phones) if p.value == old_phone]
        self.phones[index] = Phone(new_phone)
        print("Phone number updated.")

    def find_phone(self, phone):
        if not phone:
            print("Phone numbers entered incorrectly.")
            return
        for p in self.phones:
            if p.value == phone:
                print("Phone number found.")
                return p.value
        print("Phone number not found.")
        return None

    def delete_phone(self, phone):
        if not phone or len(phone) != 10:
            print("Phone numbers entered incorrectly.")
            return
        [index] = [i for i, p in enumerate(self.phones) if p.value == phone]
        del self.phones[index]
        print("Phone number deleted.")
        return phone


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not isinstance(record, Record):
            print("In AddressBook, you can append only an object of the Record class.")
            return
        name_key = record.name.value
        if not name_key:
            print("You cannot add a contact without a name to AddressBook.")
            return
        if name_key in self.data:
            print("Contact with that name already exists.")
            return
        self.data[name_key] = record
        return self.data[name_key]

    def find(self, name):
        if not name in self.data:
            print("Contact with this name not found.")
            return None
        return self.data[name]

    def delete(self, name):
        if not name:
            print("Name entered incorrectly.")
            return
        if name in self.data:
            contact = self.data[name]
            del self.data[name]
            print(f"Contact named {name} deleted.")
            return contact


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
john.delete_phone("1112223333")

for name, record in book.data.items():
    print(record)
