from backend.m1_pesanan import Array, STATUS


class Stack:

    def __init__(self):
        self.items = Array()

    def push(self, x):
        self.items.append(x)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.delete(self.items.size - 1)

    def peek(self):
        if self.is_empty():
            return None
        return self.items.get(self.items.size - 1)

    def is_empty(self):
        return self.items.size == 0

    def size(self):
        return self.items.size


def teks_array(arr):
    if isinstance(arr, Stack):
        arr = arr.items
    hasil = ""
    for i in range(arr.size):
        hasil += str(arr.get(i)) + " "
    return hasil.strip()


def rupiah(x):
    return "Rp " + f"{x:,}".replace(",", ".")


def adalah_operator(t):
    return t == "+" or t == "-" or t == "*" or t == "/"


def derajat(op):
    if op == "*" or op == "/":
        return 2
    if op == "+" or op == "-":
        return 1
    return 0


def pecah_token(ekspresi):
    tokens = Array()
    angka = ""
    for ch in ekspresi:
        if "0" <= ch <= "9":
            angka += ch
        else:
            if angka != "":
                tokens.append(angka)
                angka = ""
            if adalah_operator(ch) or ch == "(" or ch == ")":
                tokens.append(ch)
            elif ch != " ":
                raise ValueError("karakter tidak dikenal: " + ch)
    if angka != "":
        tokens.append(angka)
    return tokens


def baris_langkah(no, token, aksi, stack, output):
    return f"{no:<8}{token:<8}{aksi:<30}{teks_array(stack):<14}{teks_array(output)}"


def ke_postfix(ekspresi):
    tokens = pecah_token(ekspresi)
    stack = Stack()
    output = Array()
    langkah = Array()

    for k in range(tokens.size):
        t = tokens.get(k)
        if t == "(":
            stack.push(t)
            aksi = "push ("
        elif t == ")":
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())
            if stack.is_empty():
                raise ValueError("kurung tidak seimbang")
            stack.pop()
            aksi = "pop sampai (, buang ("
        elif adalah_operator(t):
            while (not stack.is_empty() and stack.peek() != "("
                   and derajat(stack.peek()) >= derajat(t)):
                output.append(stack.pop())
            stack.push(t)
            aksi = "push " + t
        else:
            output.append(t)
            aksi = "angka, langsung keluar"
        langkah.append(baris_langkah("1." + str(k + 1), t, aksi, stack, output))

    while not stack.is_empty():
        t = stack.pop()
        if t == "(":
            raise ValueError("kurung tidak seimbang")
        output.append(t)
    langkah.append(baris_langkah("1.akhir", "-", "pop sisa stack", stack, output))
    return output, langkah


def operasi(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    hasil = a / b
    if hasil == int(hasil):
        return int(hasil)
    return hasil


def hitung(postfix):
    stack = Stack()
    langkah = Array()
    for k in range(postfix.size):
        t = postfix.get(k)
        if adalah_operator(t):
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                raise ValueError("ekspresi tidak valid")
            hasil = operasi(a, b, t)
            stack.push(hasil)
            aksi = f"pop {b} dan {a} -> {a}{t}{b} = {hasil}"
        else:
            stack.push(int(t))
            aksi = "push " + t
        langkah.append(f"{'2.' + str(k + 1):<8}{t:<8}{aksi:<36}{teks_array(stack)}")
    total = stack.pop()
    if total is None or not stack.is_empty():
        raise ValueError("ekspresi tidak valid")
    return total, langkah


class AntreanNaif:

    def __init__(self):
        self.data = Array()
        self.total_geser = 0

    def panjang(self):
        return self.data.size

    def enqueue(self, x):
        self.data.append(x)

    def dequeue(self):
        if self.data.size == 0:
            return None
        self.total_geser += self.data.size - 1
        return self.data.delete(0)

    def push_front(self, x):
        self.total_geser += self.data.size
        self.data.insert(0, x)

    def pop_back(self):
        if self.data.size == 0:
            return None
        return self.data.delete(self.data.size - 1)


class AntreanMelingkar:

    def __init__(self, kapasitas=4):
        self.data = [None] * kapasitas
        self.K = kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0

    def panjang(self):
        return self.count

    def is_empty(self):
        return self.count == 0

    def _grow(self):
        baru = [None] * (self.K * 2)
        for i in range(self.count):
            baru[i] = self.data[(self.front + i) % self.K]
        self.data = baru
        self.front = 0
        self.rear = self.count
        self.K = self.K * 2

    def enqueue(self, x):
        if self.count == self.K:
            self._grow()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.K
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.K
        self.count -= 1
        return x

    def push_front(self, x):
        if self.count == self.K:
            self._grow()
        self.front = (self.front - 1) % self.K
        self.data[self.front] = x
        self.count += 1

    def pop_back(self):
        if self.count == 0:
            return None
        self.rear = (self.rear - 1) % self.K
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x


class Layanan:

    def __init__(self):
        self.naif = AntreanNaif()
        self.circular = AntreanMelingkar()
        self.undo = Stack()
        self.redo = Stack()

    def pilih(self, versi):
        if versi == "naif":
            return self.naif
        return self.circular

    def isi_dari(self, arr):
        for i in range(arr.size):
            p = arr.get(i)
            if p[STATUS] == "ANTRE":
                self.naif.enqueue(p)
                self.circular.enqueue(p)

    def enqueue(self, p):
        self.naif.enqueue(p)
        self.circular.enqueue(p)
        self.undo.push(("ENQUEUE", "kedua", p))
        self.redo = Stack()

    def dequeue(self, versi, n):
        antrean = self.pilih(versi)
        keluar = Array()
        for _ in range(n):
            x = antrean.dequeue()
            if x is None:
                break
            keluar.append(x)
        self.undo.push(("DEQUEUE", versi, keluar))
        self.redo = Stack()
        return keluar

    def undo_last(self):
        aksi = self.undo.pop()
        if aksi is None:
            return "Tumpukan undo kosong, tidak ada yang dibatalkan."
        jenis, versi, isi = aksi
        if jenis == "ENQUEUE":
            self.naif.pop_back()
            self.circular.pop_back()
            pesan = "Pembatalan enqueue: " + isi[0] + " dikeluarkan lagi dari BELAKANG."
        else:
            antrean = self.pilih(versi)
            for k in range(isi.size - 1, -1, -1):
                antrean.push_front(isi.get(k))
            pesan = f"{isi.size} pesanan dikembalikan ke DEPAN antrean {versi}."
        self.redo.push(aksi)
        return pesan

    def redo_last(self):
        aksi = self.redo.pop()
        if aksi is None:
            return "Tumpukan redo kosong, tidak ada yang diulang."
        jenis, versi, isi = aksi
        if jenis == "ENQUEUE":
            self.naif.enqueue(isi)
            self.circular.enqueue(isi)
            pesan = "Enqueue dikerjakan lagi: " + isi[0] + " masuk kembali ke belakang."
        else:
            antrean = self.pilih(versi)
            for _ in range(isi.size):
                antrean.dequeue()
            pesan = f"{isi.size} pesanan keluar lagi dari antrean {versi}."
        self.undo.push(aksi)
        return pesan

    def stats(self):
        return (f"panjang antrean : naif {self.naif.panjang()}, circular {self.circular.panjang()}\n"
                f"kapasitas circ. : {self.circular.K}\n"
                f"total geseran   : {self.naif.total_geser}\n"
                f"undo / redo     : {self.undo.size()} / {self.redo.size()}")


if __name__ == "__main__":
    post, _ = ke_postfix("( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
    print(teks_array(post))
    print(hitung(post)[0])
    print(hitung(ke_postfix("100 - 20 - 30")[0])[0])
    print(hitung(ke_postfix("100 / 5 / 2")[0])[0])

    q = AntreanMelingkar(4)
    for x in "ABC":
        q.enqueue(x)
    print(q.dequeue(), q.dequeue())
    for x in "DEF":
        q.enqueue(x)
    hasil = ""
    while not q.is_empty():
        hasil += q.dequeue()
    print(hasil, q.dequeue())
