"""Simple imitation of a local network."""

from __future__ import annotations

from dataclasses import dataclass


class Server:
    """A simple server."""

    __qty: int = 0

    def __new__(cls) -> Server:
        """Create a new instance of Server."""
        cls.__qty += 1
        return super().__new__(cls)

    def __init__(self) -> None:
        """Initialize a Server."""
        self._ip: int = self.__class__.__qty
        self._buffer: list[Data] = []
        self._router: Router | None = None

    def send_data(self, data: Data) -> None:
        """Send data to another server."""
        if not isinstance(data, Data):
            raise TypeError("Data must be an instance of Data class")

        if self._router is None:
            raise ValueError("Router is not linked to the server")

        self._router.incoming(data)

    def get_data(self) -> list[Data]:
        """Get data from the server."""
        current_buffer: list[Data] = self._buffer
        self._buffer = []
        return current_buffer

    def get_ip(self) -> int:
        """Get the server's IP address."""
        return self._ip


class Router:
    """A simple router."""

    def __init__(self):
        """Initialize a Router."""
        self._linked_servers: dict[int, Server] = {}
        self._buffer: list[Data] = []

    def link(self, server: Server) -> None:
        """Link a server to the router."""
        if not isinstance(server, Server):
            raise TypeError("Server must be an instance of Server class")

        serv_ip: int = server.get_ip()
        if serv_ip in self._linked_servers:
            print("WARNING: Server is already linked to the router")
            return

        self._linked_servers[serv_ip] = server
        server._router = self

    def unlink(self, server: Server) -> None:
        """Unlink a server from the router."""
        if not isinstance(server, Server):
            raise TypeError("Server must be an instance of Server class")

        if not server.get_ip() in self._linked_servers:
            raise ValueError("Server is not linked to the router")

        del self._linked_servers[server.get_ip()]
        server._router = None

    def send_data(self) -> None:
        """Send all data from local buffer to servers.

        Clear the buffer after sending.
        """
        if not self._buffer:
            print("WARNING: No data in the buffer")
            return

        for data in self._buffer:
            recipient: Server | None = self._linked_servers.get(data.ip, None)
            if not recipient:
                print(
                    f"ERROR: No linked server with IP {data.ip}. "
                    "Data is not sent."
                )
                continue

            recipient._buffer.append(data)  # непосредственно отправка данных

        self._buffer = []  # очистка буфера маршрутизатора

    def incoming(self, data: Data) -> None:
        """Save incoming data from the server to the buffer."""
        self._buffer.append(data)


@dataclass
class Data:
    """A simple data packet."""

    data: str
    ip: int  # IP-адрес сервера-получателя


if __name__ == "__main__":
    router = Router()
    sv_from = Server()
    sv_from2 = Server()

    router.link(sv_from)
    router.link(sv_from2)
    router.link(Server())
    router.link(Server())

    sv_to = Server()
    router.link(sv_to)

    sv_from.send_data(Data("Hello", sv_to.get_ip()))
    sv_from2.send_data(Data("Hello", sv_to.get_ip()))
    sv_to.send_data(Data("Hi", sv_from.get_ip()))

    print(f"#1 {router._buffer=}")

    router.send_data()

    msg_lst_from = sv_from.get_data()
    msg_lst_to = sv_to.get_data()

    print(f"{msg_lst_from=}")
    print(f"{msg_lst_to=}")
    print(f"#2 {router._buffer=}")
    print(f"{router._linked_servers=}")
