"""Pytest tests for the simple local network simulation."""

import pytest

from block_01.task_03_local_net import Data, Router, Server


def test_send_data_without_router() -> None:
    """Проверка вызова ошибок в коде.

    - Ошибка при попытке отправить объект не класса Data.
    - Ошибка при попытке отправить данные без привязки к роутеру.
    """
    server = Server()
    data_packet = Data("some secret data", 1)

    with pytest.raises(TypeError):
        server.send_data("no Data instance")  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        server.send_data(data_packet)


def test_link_and_unlink() -> None:
    """Проверка создания связи роутера с сервером и отключения этой связи.

    После попытки отвязать не связанный сервер,
    должна возникать ошибка ValueError.
    """
    router = Router()
    server = Server()

    router.link(server)
    assert server._router is router
    assert server.get_ip() in router._linked_servers

    router.unlink(server)
    assert server._router is None
    assert server.get_ip() not in router._linked_servers

    with pytest.raises(ValueError):
        router.unlink(server)


def test_router_send_data() -> None:
    """Проверка отправки данных.

    Проверяю сценарий отправки данных от сервера-отправителя роутеру,
    затем от роутера серверу-получателю.
    """
    router = Router()
    sender = Server()
    recipient = Server()
    message = "test"

    router.link(sender)
    router.link(recipient)

    data = Data(message, recipient.get_ip())

    sender.send_data(data)
    assert router._buffer == [data]

    router.send_data()
    assert router._buffer == []

    received_data = recipient.get_data()

    assert len(received_data) == 1
    assert received_data[0].data == message
    assert received_data[0].ip == recipient.get_ip()
