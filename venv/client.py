from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == "localhost":
            host = "127.0.0.1"
        self.id = host, port
        self.address = None
        self.server = host, 9999
        print("Working on id: ", self.id)

    def startProtocol(self):
        print("Sending 'ready' to server at:", self.server)
        self.transport.write('ready'.encode('utf-8'), self.server)

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')
        print("Received from server:", datagram)
        if "List of available clients:" in datagram:
            print(datagram)
            self.choose_client()
        else:
            print(addr, ":", datagram)

    def choose_client(self):
        print("Choose a client to connect to:")
        self.address = input("Write host:"), int(input("Write port:"))
        reactor.callInThread(self.send_message)

    def send_message(self):
        while True:
            self.transport.write(input(":::").encode('utf-8'), self.address)


if __name__ == "__main__":
    reactor.listenUDP(0, Client('localhost', 0))
    reactor.run()
