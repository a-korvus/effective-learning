"""Some tests for checking of custom double list implementation."""

from block_01.double_list import LinkedList, ObjectList


def test_empty_list() -> None:
    """Создание нового связного списка."""
    ll = LinkedList()
    assert ll.head is None
    assert ll.tail is None
    assert ll.get_data() is None


def test_add_single_node() -> None:
    """Добавления нового узла в пустой связный список."""
    ll = LinkedList()
    node = ObjectList("node1")
    ll.add_obj(node)

    assert ll.head is node
    assert ll.tail is node
    assert node.get_next() is None
    assert node.get_prev() is None
    assert ll.get_data() == ["node1"]


def test_add_multiple_nodes() -> None:
    """Обработка нескольких узлов в связном списке.

    Добавление узлов в список. Проверка их интеграции друг с другом.
    """
    ll = LinkedList()
    node1 = ObjectList("first")
    node2 = ObjectList("second")
    node3 = ObjectList("third")

    ll.add_obj(node1)
    ll.add_obj(node2)
    ll.add_obj(node3)

    assert ll.head is node1
    assert ll.tail is node3

    assert node1.get_next() is node2
    assert node2.get_next() is node3
    assert node3.get_next() is None

    assert node2.get_prev() is node1
    assert node3.get_prev() is node2
    assert node1.get_prev() is None

    assert ll.get_data() == ["first", "second", "third"]


def test_remove_from_empty_list() -> None:
    """Удаление узла из пустого связного списка. Проверка отсутствия ошибок."""
    ll = LinkedList()
    ll.remove_obj()

    assert ll.head is None
    assert ll.tail is None
    assert ll.get_data() is None


def test_remove_single_node() -> None:
    """Удаление единственного узла из связного списка."""
    ll = LinkedList()
    node = ObjectList("node1")
    ll.add_obj(node)

    assert ll.head is node

    ll.remove_obj()

    assert ll.head is None
    assert ll.tail is None
    assert ll.get_data() is None
