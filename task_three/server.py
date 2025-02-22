

class Server:
    _next_ip = 1

    def __init__(self):
        self.ip = Server._next_ip
        Server._next_ip += 1

        self.buffer = []
        self.router = None


    def send_data(self, data):
        if self.router:
            self.router.buffer.append(data)


    def get_data(self):
        received_data = self.buffer[:]
        self.buffer.clear()
        return received_data


    def get_ip(self):
        return self.ip


