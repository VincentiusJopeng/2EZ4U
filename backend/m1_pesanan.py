class Array:
    def __init__(self, capacity=4):
        self.data = [None] * capacity
        self.capacity = capacity
        self.size = 0

    def get(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of bounds")
        return self.data[i]

    def append(self, v):
        if self.size >= self.capacity:
            self._grow()
        self.data[self.size] = v
        self.size += 1

    def insert(self, i, v):
        if i < 0 or i > self.size:
            raise IndexError("Index out of bounds")
        if self.size >= self.capacity:
            self._grow()
        for j in range(self.size, i, -1):
            self.data[j] = self.data[j - 1]
        self.data[i] = v
        self.size += 1

    def _grow(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

if __name__ == "__main__":
    a = Array()
    b = Array()
    b.append("A")
    b.append("B")
    b.append("C")
    b.insert(0, "VIP")
    b.insert(2, "P")
    for k in range(b.size):
        print(b.get(k), end=" ")
    print()
    for i in range(10):
        a.append("O-00" + str(i))
    print(a.get(0), a.get(9))
    print(a.size, a.capacity)
    