class Router:
    def __init__(self):
        self.servers = {}
        self.buffer = []


    def link(self, server):
        self.servers[server.get_ip()] = server
        server.router = self


    def unlink(self, server):
        if server.get_ip() in self.servers:
            del self.servers[server.get_ip()]
            server.router = None


    def send_data(self):
        for data in self.buffer:
            if data.ip in self.servers:
                self.servers[data.ip].buffer.append(data)
        self.buffer.clear()
