class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def is_empty(self):
        return self.size == 0
    
    def enqueue(self, data=None):
        if data is None:
            return
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            removed_data = self.head.data
            self.head = self.head.next
            self.size -= 1
            if self.head is None:
                self.tail = None
            return removed_data
    
    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data
    
    def display(self):
        if self.is_empty:
            return None
        else:
            current = self.head
            value = []
            while current:
                value.append(current.data)
                current = current.next
            return value
        