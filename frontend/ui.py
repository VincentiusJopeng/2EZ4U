import os
import time
import traceback
import tkinter as tk

from backend.m1_pesanan import (baca_pesanan, buat_linkedlist, pesanan_baru,
                                teks_pesanan, teks_baris, JUDUL_TABEL)
from backend.m2_antrean import ke_postfix, hitung, Layanan, teks_array, rupiah
from backend.m3_laporan import (Penghitung, insertion_sort, merge_sort, linear_search,
                                binary_search, pilih_kunci, array_ke_list, kunci_oid,
                                BATAS_INSERTION)

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PESANAN = os.path.join(FOLDER, "data", "pesanan.csv")

MENUS = [
    ("DATA", "Load", "load", []),

    ("M1 - ARRAY", "Lihat pesanan", "array_get", [("Indeks", "0")]),
    ("M1 - ARRAY", "Tambah REGULER", "array_reguler", [("Nama pelanggan", "Pelanggan Baru")]),
    ("M1 - ARRAY", "Tambah PRIORITAS", "array_prioritas", [("Nama pelanggan", "Pelanggan Baru")]),
    ("M1 - ARRAY", "Tambah VIP", "array_vip", [("Nama pelanggan", "Pelanggan Baru")]),
    ("M1 - ARRAY", "Hapus pesanan", "array_hapus", [("Indeks", "0")]),

    ("M1 - LINKED LIST", "Lihat pesanan", "ll_get", [("Indeks", "0")]),
    ("M1 - LINKED LIST", "Tambah REGULER", "ll_reguler", [("Nama pelanggan", "Pelanggan Baru")]),
    ("M1 - LINKED LIST", "Tambah PRIORITAS", "ll_prioritas", [("Nama pelanggan", "Pelanggan Baru")]),
    ("M1 - LINKED LIST", "Tambah VIP", "ll_vip", [("Nama pelanggan", "Pelanggan Baru")]),
    ("M1 - LINKED LIST", "Hapus pesanan", "ll_hapus", [("Indeks", "0")]),

    ("M2 - STACK DAN QUEUE", "Postfix (mesin kasir)", "stack_postfix",
     [("Struk (infix)", "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")]),
    ("M2 - STACK DAN QUEUE", "Undo", "stack_undo", []),
    ("M2 - STACK DAN QUEUE", "Redo", "stack_redo", []),
    ("M2 - STACK DAN QUEUE", "Queue - enqueue", "queue_enqueue", [("Nama pelanggan", "X2")]),
    ("M2 - STACK DAN QUEUE", "Queue - dequeue naif", "queue_dequeue_naive", [("Berapa kali", "1")]),
    ("M2 - STACK DAN QUEUE", "Queue - dequeue circular", "queue_dequeue_circular", [("Berapa kali", "1")]),

    ("M3 - SORT DAN SEARCH", "Insertion sort", "insertion_sort",
     [("Jumlah baris", "1000"), ("Kunci (oid/harga/selesai)", "harga")]),
    ("M3 - SORT DAN SEARCH", "Merge sort", "merge_sort",
     [("Jumlah baris", "1000"), ("Kunci (oid/harga/selesai)", "harga")]),
    ("M3 - SORT DAN SEARCH", "Linear search", "linear_search", [("oid", "O-137442")]),
    ("M3 - SORT DAN SEARCH", "Binary search", "binary_search", [("oid", "O-137442")]),
]


class App:
    def __init__(self, root):
        root.title("2EZ4U Food Delivery")
        root.geometry("1150x720")
        self.cmd = None
        self.entries = []

        self.array = None
        self.ll = None
        self.layanan = None
        self.daftar = None
        self.urut_oid = None
        self.nomor = 200000

        left = tk.Frame(root, padx=8, pady=4)
        left.pack(side="left", fill="y")
        section = ""
        for menu in MENUS:
            if menu[0] != section:
                section = menu[0]
                tk.Label(left, text=section, font=("Arial", 8, "bold")).pack(anchor="w", pady=(6, 0))
            tk.Button(left, text=menu[1], width=24, anchor="w", font=("Arial", 8), pady=0,
                      command=lambda m=menu: self.open_menu(m)).pack()

        right = tk.Frame(root, padx=8, pady=8)
        right.pack(side="left", fill="both", expand=True)

        self.title = tk.Label(right, text="Klik Load dulu, lalu pilih menu", font=("Arial", 14, "bold"))
        self.title.pack(anchor="w")

        self.form = tk.Frame(right)
        self.form.pack(anchor="w", pady=8)

        self.output = tk.Text(right, height=20, font=("Consolas", 9), wrap="none")
        self.output.pack(fill="both", expand=True)

        tk.Label(right, text="COMMAND").pack(anchor="w")
        self.log = tk.Text(right, height=6, font=("Consolas", 9))
        self.log.pack(fill="x")

    def open_menu(self, menu):
        section, name, cmd, fields = menu
        self.cmd = cmd
        self.title.config(text=section + " : " + name)

        for w in self.form.winfo_children():
            w.destroy()
        self.entries = []

        for label, default in fields:
            tk.Label(self.form, text=label).pack(side="left")
            e = tk.Entry(self.form, width=max(12, len(default) + 4))
            e.insert(0, default)
            e.pack(side="left", padx=(4, 12))
            self.entries.append(e)
        tk.Button(self.form, text="JALANKAN", command=self.run_cmd).pack(side="left")

    def run_cmd(self):
        values = []
        for e in self.entries:
            values.append(e.get().strip())

        start = time.perf_counter()
        try:
            result = self.handle(self.cmd, values)
        except Exception as err:
            traceback.print_exc()
            result = "ERROR: " + str(err)
        ms = (time.perf_counter() - start) * 1000

        self.output.delete("1.0", "end")
        self.output.insert("end", result)
        self.log.insert("1.0", f"{self.cmd:<24} {ms:10.2f} ms\n")


    def handle(self, cmd, values):
        if cmd == "load":
            return self.load()
        if self.array is None:
            return "Klik menu Load dulu."
        if cmd.startswith("array_") or cmd.startswith("ll_"):
            return self.menu_m1(cmd, values)
        if cmd.startswith("stack_") or cmd.startswith("queue_"):
            return self.menu_m2(cmd, values)
        return self.menu_m3(cmd, values)

    def load(self):
        self.array = baca_pesanan(DATA_PESANAN)
        self.ll = buat_linkedlist(self.array)
        self.layanan = Layanan()
        self.layanan.isi_dari(self.array)
        self.daftar = array_ke_list(self.array, self.array.size)
        self.urut_oid = None
        return (f"{self.array.size} pesanan dimuat ke Array dan Linked List.\n"
                f"{self.layanan.naif.panjang()} pesanan berstatus ANTRE masuk ke KEDUA antrean.")

    def oid_baru(self):
        self.nomor += 1
        return f"O-{self.nomor:06d}"

    def menu_m1(self, cmd, values):
        if cmd.startswith("array_"):
            s = self.array
            aksi = cmd[len("array_"):]
        else:
            s = self.ll
            aksi = cmd[len("ll_"):]

        if aksi == "get":
            i = int(values[0])
            return f"Pesanan ke-{i} dari {s.size}:\n\n" + teks_pesanan(s.get(i))

        if aksi == "hapus":
            i = int(values[0])
            p = s.delete(i)
            return f"Pesanan ke-{i} dihapus. Sisa {s.size} pesanan.\n\n" + teks_pesanan(p)

        nama = values[0] or "Pelanggan Baru"
        if aksi == "reguler":
            p = pesanan_baru(self.oid_baru(), nama, 3)
            posisi = s.size
            s.append(p)
        elif aksi == "prioritas":
            p = pesanan_baru(self.oid_baru(), nama, 2)
            posisi = s.size // 2
            s.insert(posisi, p)
        else:
            p = pesanan_baru(self.oid_baru(), nama, 1)
            posisi = 0
            s.insert(0, p)
        return f"{p[0]} masuk di posisi {posisi}. Jumlah sekarang {s.size}.\n\n" + teks_pesanan(p)

    def menu_m2(self, cmd, values):
        L = self.layanan

        if cmd == "stack_postfix":
            postfix, langkah1 = ke_postfix(values[0])
            total, langkah2 = hitung(postfix)
            teks = (f"Struk   : {values[0]}\n"
                    f"Postfix : {teks_array(postfix)}\n"
                    f"TOTAL   : {rupiah(total)}\n\n"
                    f"{'langkah':<8}{'token':<8}{'tindakan':<30}{'stack':<14}output\n")
            for k in range(langkah1.size):
                teks += langkah1.get(k) + "\n"
            teks += f"\n{'langkah':<8}{'token':<8}{'tindakan':<36}stack nilai\n"
            for k in range(langkah2.size):
                teks += langkah2.get(k) + "\n"
            return teks

        if cmd == "stack_undo":
            return L.undo_last() + "\n\n" + L.stats()

        if cmd == "stack_redo":
            return L.redo_last() + "\n\n" + L.stats()

        if cmd == "queue_enqueue":
            p = pesanan_baru(self.oid_baru(), values[0] or "Pelanggan Baru", 2)
            L.enqueue(p)
            return f"{p[0]} masuk paling belakang di KEDUA antrean.\n\n" + L.stats()

        versi = "naif" if cmd == "queue_dequeue_naive" else "circular"
        n = int(values[0])
        geser_awal = L.naif.total_geser
        keluar = L.dequeue(versi, n)
        geser = L.naif.total_geser - geser_awal
        teks = f"{keluar.size} pesanan keluar dari antrean {versi} | {geser} elemen digeser\n\n"
        teks += JUDUL_TABEL + "\n"
        for k in range(min(keluar.size, 20)):
            teks += teks_baris(k + 1, keluar.get(k)) + "\n"
        return teks + "\n" + L.stats()

    def menu_m3(self, cmd, values):
        c = Penghitung()

        if cmd == "insertion_sort" or cmd == "merge_sort":
            n = min(int(values[0]), len(self.daftar))
            nama_kunci = values[1]
            if cmd == "insertion_sort" and n > BATAS_INSERTION:
                return f"DITOLAK: batasnya {BATAS_INSERTION} baris, pakai merge sort untuk data besar."
            A = self.daftar[:n]
            if cmd == "insertion_sort":
                A = insertion_sort(A, pilih_kunci(nama_kunci), c)
            else:
                A = merge_sort(A, pilih_kunci(nama_kunci), c)
            teks = (f"{n} pesanan diurutkan menurut {nama_kunci}.\n"
                    f"{c.banding} perbandingan, {c.pindah} pemindahan.\n\n"
                    f"10 baris pertama:\n{JUDUL_TABEL}\n")
            for k in range(min(n, 10)):
                teks += teks_baris(k + 1, A[k]) + "\n"
            return teks

        target = values[0]
        if cmd == "linear_search":
            i = linear_search(self.daftar, target, c)
            if i == -1:
                return f"{target} tidak ditemukan. {c.banding} perbandingan."
            return f"Ditemukan di indeks {i}. {c.banding} perbandingan.\n\n" + teks_pesanan(self.daftar[i])

        info = ""
        if self.urut_oid is None:
            t0 = time.perf_counter()
            self.urut_oid = merge_sort(self.daftar, kunci_oid, Penghitung())
            info = f"Daftar terurut oid dibangun sekali dengan merge sort: {(time.perf_counter() - t0) * 1000:.2f} ms.\n"
        i = binary_search(self.urut_oid, target, c)
        if i == -1:
            return info + f"{target} tidak ditemukan. {c.banding} perbandingan."
        return info + f"Ditemukan di baris {i}. {c.banding} perbandingan.\n\n" + teks_pesanan(self.urut_oid[i])


def run():
    root = tk.Tk()
    App(root)
    root.mainloop()
