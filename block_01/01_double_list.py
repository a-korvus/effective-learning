"""Custom implementation of a doubly linked list with basic operations."""

from __future__ import annotations


class LinkedList:
    """A linked list of objects."""

    def __init__(self) -> None:
        """Initialize an instance of LinkedList."""
        self.head: ObjectList | None = None
        self.tail: ObjectList | None = None

    def add_obj(self, obj: ObjectList) -> None:
        """Add an object to the end of the linked list."""
        if not self.tail:
            self.head = obj
            self.tail = obj
            return

        # для текущего хвоста устанавливаем ссылку на следующий объект
        self.tail.set_next(obj)
        # для нового хвоста устанавливаем ссылку на предыдущий объект
        obj.set_prev(self.tail)
        # обновляем хвост списка
        self.tail = obj

    def remove_obj(self) -> None:
        """Remove a last object from the LinkedList."""
        if not self.tail:
            return

        # получаем текущий предпоследний объект связного списка
        # который станет последним после удаления текущего хвоста
        penultimate: ObjectList | None = self.tail.get_prev()
        if not penultimate:
            self.head = None
            self.tail = None
            return

        # удаляем ссылку на следующий объект у предпоследнего объекта
        penultimate.set_next(None)
        # удаляем ссылку на предыдущий объект у текущего хвоста
        self.tail.set_prev(None)
        # обновляем хвост списка
        self.tail = penultimate

    def get_data(self) -> list[str] | None:
        """Get data of each object in the LinkedList."""
        if not self.head:
            return None

        all_data: list[str] = []
        current_obj: ObjectList | None = self.head
        while current_obj:
            all_data.append(current_obj.get_data())
            current_obj = current_obj.get_next()
        return all_data


class ObjectList:
    """An object in the linked list."""

    def __init__(self, data: str) -> None:
        """Initialize an instance of ObjectList."""
        self.__next: ObjectList | None = None
        self.__prev: ObjectList | None = None
        self.__data: str = data

    def set_next(self, obj: ObjectList | None) -> None:
        """Set the next object in the list."""
        self.__next = obj

    def set_prev(self, obj: ObjectList | None) -> None:
        """Set the previous object in the list."""
        self.__prev = obj

    def get_next(self) -> ObjectList | None:
        """Get the next object in the list."""
        return self.__next

    def get_prev(self) -> ObjectList | None:
        """Get the previous object in the list."""
        return self.__prev

    def set_data(self, data: str) -> None:
        """Set the data of the object."""
        self.__data = data

    def get_data(self) -> str:
        """Get the data of the object."""
        return self.__data


if __name__ == "__main__":
    lst = LinkedList()

    lst.add_obj(ObjectList("данные 1"))
    lst.add_obj(ObjectList("данные 2"))
    print(f"{lst.get_data()=}\n")

    lst.add_obj(ObjectList("данные 3"))

    print(f"{lst.get_data()=}\n")

    lst.remove_obj()
    print(f"{lst.get_data()=}\n")

    lst.remove_obj()
    print(f"{lst.get_data()=}\n")

    lst.remove_obj()
    print(f"{lst.get_data()=}\n")

    lst.remove_obj()
    print(f"{lst.get_data()=}\n")
