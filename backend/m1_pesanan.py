OID, PELANGGAN, RESTO, MENU, HARGA, PRIORITAS, MASUK, SELESAI, STATUS = 0, 1, 2, 3, 4, 5, 6, 7, 8


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

    def delete(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of bounds")
        removed = self.data[i]
        for j in range(i, self.size - 1):
            self.data[j] = self.data[j + 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return removed

    def _grow(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, v):
        node = Node(v)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def get(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(i):
            current = current.next
        return current.value

    def insert(self, i, v):
        if i < 0 or i > self.size:
            raise IndexError("Index out of bounds")
        if i == self.size:
            self.append(v)
            return
        node = Node(v)
        if i == 0:
            node.next = self.head
            self.head = node
        else:
            prev = self.head
            for _ in range(i - 1):
                prev = prev.next
            node.next = prev.next
            prev.next = node
        self.size += 1

    def delete(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of bounds")
        if i == 0:
            removed = self.head
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        else:
            prev = self.head
            for _ in range(i - 1):
                prev = prev.next
            removed = prev.next
            prev.next = removed.next
            if removed is self.tail:
                self.tail = prev
        self.size -= 1
        return removed.value


def pecah_baris(baris):
    if '"' not in baris:
        return baris.split(",")
    kolom = []
    isi = ""
    dalam_kutip = False
    for ch in baris:
        if ch == '"':
            dalam_kutip = not dalam_kutip
        elif ch == "," and not dalam_kutip:
            kolom.append(isi)
            isi = ""
        else:
            isi += ch
    kolom.append(isi)
    return kolom


def ke_pesanan(kolom):
    selesai = None
    if kolom[SELESAI] != "":
        selesai = int(kolom[SELESAI])
    return (kolom[OID], kolom[PELANGGAN], kolom[RESTO], kolom[MENU],
            int(kolom[HARGA]), int(kolom[PRIORITAS]), int(kolom[MASUK]),
            selesai, kolom[STATUS])


def baca_pesanan(path):
    arr = Array()
    with open(path, encoding="utf-8") as f:
        f.readline()
        for baris in f:
            baris = baris.strip()
            if baris != "":
                arr.append(ke_pesanan(pecah_baris(baris)))
    return arr


def buat_linkedlist(arr):
    ll = LinkedList()
    for i in range(arr.size):
        ll.append(arr.get(i))
    return ll


def pesanan_baru(oid, nama, prioritas):
    return (oid, nama, "kafe-teknik", "roti-bakar", 12000, prioritas, 0, None, "ANTRE")


def format_jam(detik):
    if detik is None:
        return "-"
    return f"{detik // 3600:02d}:{detik % 3600 // 60:02d}:{detik % 60:02d}"


def teks_pesanan(p):
    return ("oid       : " + p[OID] + "\n"
            "pelanggan : " + p[PELANGGAN] + "\n"
            "resto     : " + p[RESTO] + "\n"
            "menu      : " + p[MENU] + "\n"
            "harga     : " + str(p[HARGA]) + "\n"
            "prioritas : " + str(p[PRIORITAS]) + "\n"
            "masuk     : " + format_jam(p[MASUK]) + "\n"
            "selesai   : " + format_jam(p[SELESAI]) + "\n"
            "status    : " + p[STATUS])


def teks_baris(nomor, p):
    return (f"{nomor:<6}{p[OID]:<10}{p[PELANGGAN][:22]:<24}{p[RESTO]:<15}"
            f"{p[MENU]:<16}{p[HARGA]:>7}  {format_jam(p[SELESAI])}")


JUDUL_TABEL = f"{'#':<6}{'oid':<10}{'pelanggan':<24}{'resto':<15}{'menu':<16}{'harga':>7}  selesai"


if __name__ == "__main__":
    for S in (Array, LinkedList):
        s = S()
        s.append("A")
        s.append("B")
        s.append("C")
        s.insert(0, "VIP")
        s.insert(s.size // 2, "P")
        s.insert(s.size, "Z")
        isi = ""
        for k in range(s.size):
            isi += s.get(k) + " "
        print(S.__name__, isi)

        print(s.delete(0), s.delete(s.size - 1))
        s.append("D")
        isi = ""
        for k in range(s.size):
            isi += s.get(k) + " "
        print(S.__name__, isi)

    print(pecah_baris('O-000004,"Oskar Puspita, S.Sos",kafe-teknik,nasi-padang,25000,2,29632,,CANCEL'))
