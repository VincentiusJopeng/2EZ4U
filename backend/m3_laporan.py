from backend.m1_pesanan import OID, HARGA, SELESAI

BATAS_INSERTION = 20000


class Penghitung:
    def __init__(self):
        self.banding = 0
        self.pindah = 0


def kunci_oid(p):
    return p[OID]


def kunci_harga(p):
    return p[HARGA]


def kunci_selesai(p):
    if p[SELESAI] is None:
        return 999999999
    return p[SELESAI]


def pilih_kunci(nama):
    if nama == "harga":
        return kunci_harga
    if nama == "selesai":
        return kunci_selesai
    return kunci_oid


def array_ke_list(arr, n):
    hasil = [None] * n
    for i in range(n):
        hasil[i] = arr.get(i)
    return hasil


def insertion_sort(A, kunci, c):
    for i in range(1, len(A)):
        x = A[i]
        kx = kunci(x)
        j = i - 1
        while j >= 0:
            c.banding += 1
            if kunci(A[j]) > kx:
                A[j + 1] = A[j]
                c.pindah += 1
                j -= 1
            else:
                break
        A[j + 1] = x
    return A


def merge_sort(A, kunci, c):
    if len(A) <= 1:
        return A
    tengah = len(A) // 2
    kiri = merge_sort(A[:tengah], kunci, c)
    kanan = merge_sort(A[tengah:], kunci, c)
    return gabung(kiri, kanan, kunci, c)


def gabung(kiri, kanan, kunci, c):
    hasil = [None] * (len(kiri) + len(kanan))
    i = 0
    j = 0
    k = 0
    while i < len(kiri) and j < len(kanan):
        c.banding += 1
        if kunci(kiri[i]) <= kunci(kanan[j]):
            hasil[k] = kiri[i]
            i += 1
        else:
            hasil[k] = kanan[j]
            j += 1
        k += 1
        c.pindah += 1
    while i < len(kiri):
        hasil[k] = kiri[i]
        i += 1
        k += 1
        c.pindah += 1
    while j < len(kanan):
        hasil[k] = kanan[j]
        j += 1
        k += 1
        c.pindah += 1
    return hasil


def linear_search(A, target, c):
    for i in range(len(A)):
        c.banding += 1
        if A[i][OID] == target:
            return i
    return -1


def binary_search(A, target, c):
    lo = 0
    hi = len(A) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        c.banding += 1
        if A[mid][OID] == target:
            return mid
        if A[mid][OID] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


if __name__ == "__main__":
    def p(oid, harga):
        return (oid, "", "", "", harga, 3, 0, None, "DONE")

    data = [p("O-5", 30), p("O-2", 10), p("O-4", 20), p("O-1", 10), p("O-3", 20)]

    for nama, fungsi in (("insertion", insertion_sort), ("merge", merge_sort)):
        hasil = fungsi(list(data), kunci_harga, Penghitung())
        teks = ""
        for x in hasil:
            teks += x[OID] + " "
        print(nama, teks)

    urut = merge_sort(list(data), kunci_oid, Penghitung())
    for target in ("O-1", "O-3", "O-5", "O-9"):
        print(target, binary_search(urut, target, Penghitung()), end="  ")
    print()
    print("kosong", binary_search([], "O-1", Penghitung()))
