class Data:
    def __init__(self, msg, ip):
        self.msg = msg
        self.ip = ip

    def __str__(self):
        return f"Received message: {self.msg} from IP: {self.ip}"