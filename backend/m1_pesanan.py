class Array:
    def __init__(self, capacity=4):
        self.data = [None] * capacity
        self.capacity = capacity
        self.size = 0

    def get(self, i):
        # TODO 1: if i is smaller than 0 or i >= self.size -> raise IndexError
        # TODO 2: otherwise return the element at position i
        if i < 0 or i >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[i]

    def append(self, v):
        # TODO 1: put v in the first empty slot (which index is that? hint: self.size)
        # TODO 2: increase self.size by 1
        # (ignore "what if it's full" for now, we'll add _grow next)
        if self.size >= self.capacity:
            raise IndexError("Array is full")
        self.data[self.size] = v
        self.size += 1