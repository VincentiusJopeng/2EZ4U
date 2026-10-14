import time
import traceback
import tkinter as tk

# Daftar menu: (bagian, nama tombol, perintah, daftar input)
MENUS = [
    ("DATA", "Load", "load", []),

    ("M1 - ARRAY", "Lihat pesanan", "array_get", ["Indeks"]),
    ("M1 - ARRAY", "Tambah REGULER", "array_reguler", ["Nama pelanggan"]),
    ("M1 - ARRAY", "Tambah PRIORITAS", "array_prioritas", ["Nama pelanggan"]),
    ("M1 - ARRAY", "Tambah VIP", "array_vip", ["Nama pelanggan"]),
    ("M1 - ARRAY", "Hapus pesanan", "array_hapus", ["Indeks"]),

    ("M1 - LINKED LIST", "Lihat pesanan", "ll_get", ["Indeks"]),
    ("M1 - LINKED LIST", "Tambah REGULER", "ll_reguler", ["Nama pelanggan"]),
    ("M1 - LINKED LIST", "Tambah PRIORITAS", "ll_prioritas", ["Nama pelanggan"]),
    ("M1 - LINKED LIST", "Tambah VIP", "ll_vip", ["Nama pelanggan"]),
    ("M1 - LINKED LIST", "Hapus pesanan", "ll_hapus", ["Indeks"]),
]


class App:
    def __init__(self, root):
        root.title("2EZ4U Food Delivery")
        root.geometry("900x600")
        self.cmd = None
        self.entries = []

        # ----- KIRI: daftar menu -----
        left = tk.Frame(root, padx=8, pady=8)
        left.pack(side="left", fill="y")
        section = ""
        for menu in MENUS:
            if menu[0] != section:
                section = menu[0]
                tk.Label(left, text=section, font=("Arial", 9, "bold")).pack(anchor="w", pady=(8, 0))
            tk.Button(left, text=menu[1], width=22, anchor="w",
                      command=lambda m=menu: self.open_menu(m)).pack()

        # ----- KANAN: judul, form, hasil, log -----
        right = tk.Frame(root, padx=8, pady=8)
        right.pack(side="left", fill="both", expand=True)

        self.title = tk.Label(right, text="Pilih menu di kiri", font=("Arial", 14, "bold"))
        self.title.pack(anchor="w")

        self.form = tk.Frame(right)
        self.form.pack(anchor="w", pady=8)

        self.output = tk.Text(right, height=18, font=("Consolas", 10))
        self.output.pack(fill="both", expand=True)

        tk.Label(right, text="COMMAND").pack(anchor="w")
        self.log = tk.Text(right, height=6, font=("Consolas", 9))
        self.log.pack(fill="x")

    def open_menu(self, menu):
        """Dipanggil saat tombol menu di kiri diklik: buat form-nya."""
        section, name, cmd, fields = menu
        self.cmd = cmd
        self.title.config(text=section + " : " + name)

        for w in self.form.winfo_children():   # hapus form lama
            w.destroy()
        self.entries = []

        for label in fields:
            tk.Label(self.form, text=label).pack(side="left")
            e = tk.Entry(self.form, width=20)
            e.pack(side="left", padx=(4, 12))
            self.entries.append(e)
        tk.Button(self.form, text="JALANKAN", command=self.run_cmd).pack(side="left")

    def run_cmd(self):
        """Dipanggil saat tombol JALANKAN diklik: jalankan + ukur waktu."""
        values = []
        for e in self.entries:
            values.append(e.get())

        start = time.perf_counter()
        try:
            result = self.handle(self.cmd, values)
        except Exception as err:
            traceback.print_exc()               # error lengkap muncul di terminal
            result = "ERROR: " + str(err)
        ms = (time.perf_counter() - start) * 1000

        self.output.delete("1.0", "end")
        self.output.insert("end", result)
        self.log.insert("1.0", f"{self.cmd:<20} {ms:8.2f} ms\n")

    def handle(self, cmd, values):
        """Sambungkan backend di sini. Satu if per menu, kembalikan teks hasil."""
        # Contoh nanti:
        # if cmd == "array_get":
        #     p = self.array.get(int(values[0]))
        #     return str(p)
        return "Menu '" + cmd + "' belum dibuat.\nInput: " + str(values)


def run():
    root = tk.Tk()
    App(root)
    root.mainloop()