import socket

HOST, PORT = "localhost", 9999


class ClientInfo:

    def __init__(self, conn):
        self.sock = conn

    def data_travel(self, customer_data, action):
        self.sock.sendall(bytes(customer_data + "|" + action + "\n", "utf-8"))
        return str(self.sock.recv(1024), "utf-8")

    def find_customer(self):
        customer_name = input("Enter customer name: ")
        response = self.data_travel(customer_name, "find_customer")
        print(f"Server response: {response}")

    def add_customer(self):
        name = input("Enter the new customer name: ")
        age = input("Enter the new customer age: ")
        address = input("Enter the new customer address: ")
        phone = input("Enter the new customer phone number: ")
        new_customer_data = f"{name}%{age}%{address}%{phone}"
        response = self.data_travel(new_customer_data, "add_customer")
        print(f"Server response: {response}")

    def delete_customer(self):
        customer_to_remove = input("Enter the name of the customer you wish to delete: ")
        response = self.data_travel(customer_to_remove, "delete_customer")
        print(f"Server response: {response}")

    def update_customer_age(self):
        name = input("Enter the name of the customer you wish to update: ")
        age = input("Enter the age of the customer: ")
        customer_update = f"{name}%{age}"
        response = self.data_travel(customer_update, "update_customer_age")
        print(f"Server response: {response}")

    def update_customer_address(self):
        name = input("Enter the name of the customer you wish to update: ")
        address = input("Enter the address of the customer: ")
        customer_update = f"{name}%{address}"
        response = self.data_travel(customer_update, "update_customer_address")
        print(f"Server response: {response}")

    def update_customer_phone(self):
        name = input("Enter the name of the customer you wish to update: ")
        phone = input("Enter the phone number of the customer: ")
        customer_update = f"{name}%{phone}"
        response = self.data_travel(customer_update, "update_customer_phone")
        print(f"Server response: {response}")

    def print_report(self):
        print("** Python DB contents **")
        response = self.data_travel("", "print_report")
        print(response)


def menu(client):
    print("""Python DB Menu \n
    1. Find customer
    2. Add customer
    3. Delete customer
    4. Update customer age
    5. Update customer address
    6. Update customer phone
    7. Print report
    8. Exit 
    """)
    user_input = input("Select: ")

    while user_input != "8":
        if user_input == "1":
            client.find_customer()
        elif user_input == "2":
            client.add_customer()
        elif user_input == "3":
            client.delete_customer()
        elif user_input == "4":
            client.update_customer_age()
        elif user_input == "5":
            client.update_customer_address()
        elif user_input == "6":
            client.update_customer_phone()
        elif user_input == "7":
            client.print_report()
        else:
            print("Wrong input")
            print("You must select a number between 1 and 8.")
        user_input = input("Select: ")
    print("Exit program...")


if __name__ == "__main__":
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        client_info = ClientInfo(sock)
        menu(client_info)
