import socketserver


class Customer:

    def __init__(self, name, age, address, phone):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone

    def __repr__(self):
        return f"{self.name}|{self.age}|{self.address}|{self.phone}"

    def __lt__(self, other):
        return self.name < other.name


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    lines = open("data.txt", "r").readlines()
    database = {}
    for line in lines:
        customer = Customer(*tuple(field.strip() for field in line.split("|")))
        database[customer.name] = customer

    # for key, customer in database.items():
    #     print(f"{key}: {customer}")

    def find_customer(self, customer_name):
        try:
            return str(self.database[customer_name])
        except KeyError:
            return f"{customer_name} not found in database"

    def add_customer(self, params):
        customer = Customer(*params.split("%"))
        if customer.name == "":
            return "Customer must have a name!"
        if customer.name in self.database.keys():
            return "Customer already exists"
        self.database[customer.name] = customer
        return "Customer has been added"

    def delete_customer(self, customer_name):
        if customer_name == "":
            return "Customer must have a name!"
        try:
            del self.database[customer_name]
            return f"{customer_name} has been deleted successfully."
        except KeyError:
            return f"{customer_name} does not exist."

    def update_customer_age(self, params):
        name, new_age = params.split("%")
        if name == "":
            return "Customer must have a name!"
        if name in self.database.keys():
            self.database[name].age = new_age
            return f"{name}'s age has been updated successfully. "
        else:
            return "Customer not found."

    def update_customer_address(self, params):
        name, new_address = params.split("%")
        if name == "":
            return "Customer must have a name!"
        if name in self.database.keys():
            self.database[name].address = new_address
            return f"{name}'s address has been updated successfully. "
        else:
            return "Customer not found."

    def update_customer_phone(self, params):
        name, new_phone = params.split("%")
        if name == "":
            return "Customer must have a name!"
        if name in self.database.keys():
            self.database[name].phone = new_phone
            return f"{name}'s phone has been updated successfully. "
        else:
            return "Customer not found."

    def print_report(self, params):
        return "\n".join([str(customer) for customer in sorted(self.database.values())])

    def handle(self):
        actions = {}
        actions["find_customer"] = lambda x: self.find_customer(x)
        actions["add_customer"] = lambda x: self.add_customer(x)
        actions["delete_customer"] = lambda x: self.delete_customer(x)
        actions["update_customer_age"] = lambda x: self.update_customer_age(x)
        actions["update_customer_address"] = lambda x: self.update_customer_address(x)
        actions["update_customer_phone"] = lambda x: self.update_customer_phone(x)
        actions["print_report"] = lambda x: self.print_report(x)
        # self.request is the TCP socket connected to the client
        while True:
            params, action = str(self.request.recv(1024).strip(), "utf-8").split("|")
            response = actions[action](params)
            # send back the data to the client
            self.request.sendall(response.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

