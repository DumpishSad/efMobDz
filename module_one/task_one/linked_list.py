from obj_list import ObjList


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None


    def add_obj(self, obj):
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            obj.prev = self.tail
            self.tail.next = obj
            self.tail = obj


    def remove_obj(self):
        if self.head is None:
            return

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None


    def get_data(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next
        return result
