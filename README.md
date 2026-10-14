# 2EZ4U APP

Proyek Struktur Data & Analisa Algoritma

Proyek ini berisi backend aplikasi layanan antar makanan versi sederhana (seperti GoFood) yang menggunakan data 200.000 pesanan dari file CSV.

- Nama: Vincentius Jopeng
- NRP: 5024251120

Progress saat ini:
- M1
- M2
- M3


## Cara Menjalankan

Program ini membutuhkan Python 3.11 atau lebih baru. Tidak ada library tambahan yang perlu diinstal karena Tkinter sudah termasuk dalam Python.
```
python app.py
```

Setelah jendela terbuka, klik menu `Load` terlebih dahulu untuk membaca data, lalu pilih menu di sebelah kiri dan klik `JALANKAN`.
Kotak COMMAND di bagian bawah mencatat setiap perintah yang dijalankan beserta waktunya.

Untuk menguji backend tanpa UI, jalankan perintah berikut dari folder utama:

```
python -m backend.m1_pesanan
python -m backend.m2_antrean
python -m backend.m3_laporan
```


## Struktur Folder

```
2EZ4U/
|-- app.py              -> program utama
|-- data/               -> pesanan.csv dan peta.csv
|-- backend/
|   |-- m1_pesanan.py   -> M1: array, linked list, dan pembaca CSV
|   |-- m2_antrean.py   -> M2: stack dan queue
|   |-- m3_laporan.py   -> M3: sort dan search
|-- frontend/
|   |-- ui.py           -> antarmuka Tkinter
```

Sesuai aturan proyek, saya tidak menggunakan dict, set, sorted, .sort(), heapq, bisect, maupun collections.
List hanya digunakan sebagai array biasa.

Alur program: app.py membuka ui.py. Ketika tombol diklik, fungsi handle() memanggil fungsi yang sesuai di backend, lalu hasilnya ditampilkan di layar.


## M1 - Array vs Linked List

Data pesanan disimpan di dua struktur sekaligus agar performanya bisa dibandingkan.

Array:
- Ketika array penuh, kapasitasnya dikali 2 lalu seluruh isinya disalin. Proses menyalin memang O(n), tetapi jarang terjadi, sehingga rata-rata append tetap O(1) (amortized).
- Pada insert, elemen digeser mulai dari belakang. Jika digeser dari depan, data akan tertimpa sebelum sempat dipindahkan.
- Pada delete, elemen setelah posisi yang dihapus digeser satu langkah ke kiri.

Linked List:
- Setiap pesanan disimpan dalam sebuah Node yang berisi value dan next.
- Saya menyimpan head dan tail. Tail digunakan agar penambahan di belakang tidak perlu menelusuri list dari depan.
- Untuk insert di tengah, program menelusuri sampai node sebelum posisi tujuan, lalu menyambungkan node baru ke sisa list terlebih dahulu, baru kemudian mengubah prev.next. Jika urutannya terbalik, sisa list akan hilang.
- Jika node yang dihapus adalah node terakhir, tail juga harus dipindahkan ke node sebelumnya.

Untuk membaca CSV, saya membuat parser sendiri karena ada nama pelanggan yang mengandung koma di dalam tanda kutip, misalnya "Oskar Puspita, S.Sos". Jika hanya menggunakan split(","), kolomnya akan bergeser.

Kompleksitas:

| Operasi | Array | Linked List |
|---|---|---|
| Lihat pesanan ke-i | O(1) | O(n) |
| Tambah REGULER (belakang) | O(1) amortized | O(1) |
| Tambah PRIORITAS (tengah) | O(n) | O(n) |
| Tambah VIP (depan) | O(n) | O(1) |
| Hapus pesanan ke-i | O(n) | O(n) |

Hasil pengukuran waktu pada laptop saya (200.000 data):

| Operasi | Array | Linked List |
|---|---|---|
| Lihat pesanan ke-100000 | 0.29 ms | 1.97 ms |
| Tambah REGULER | 0.02 ms | 0.01 ms |
| Tambah PRIORITAS | 5.11 ms | 1.91 ms |
| Tambah VIP | 9.21 ms | 0.01 ms |
| Hapus pesanan ke-0 | 9.18 ms | 0.01 ms |

Perbedaan paling terlihat pada tambah VIP dan hapus dari depan. Array harus menggeser seluruh elemen, sedangkan linked list cukup mengubah head.


## M2 - Stack & Queue

Stack dibuat di atas Array dari M1, dengan operasi push, pop, peek, dan is_empty.

Mesin kasir:
- Struk dalam bentuk infix diubah ke postfix menggunakan stack, kemudian postfix tersebut dihitung juga menggunakan stack.
- Contoh: ( 3 * 12000 ) + ( 2 * 8500 ) - 5000 menjadi 3 12000 * 2 8500 * + 5000 - dengan total Rp 48.000.
- Saat menghitung, nilai yang di-pop pertama adalah operand kanan. Karena itu b = pop() dilakukan lebih dulu, lalu a = pop(), kemudian dihitung a - b. Jika urutannya terbalik, 100 - 20 - 30 akan menghasilkan nilai yang salah (seharusnya 50).

Undo dan redo:
- Setiap aksi antrean (enqueue dan dequeue) disimpan ke stack undo beserta data pesanannya.
- Undo enqueue berarti mengeluarkan kembali pesanan dari belakang antrean.
- Undo dequeue berarti mengembalikan pesanan ke depan antrean, bukan ke belakang.
- Redo menjalankan ulang aksi aslinya.
- Ketika ada aksi baru, stack redo dikosongkan. Jika tidak, redo dapat menerapkan aksi lama pada keadaan antrean yang sudah berbeda.

Queue dibuat dalam dua versi, dan keduanya diisi dengan 19.850 pesanan berstatus ANTRE yang sama:
- Versi naif: dequeue mengambil indeks 0 lalu menggeser seluruh sisa elemen ke kiri, sehingga O(n).
- Versi melingkar (circular): hanya pointer front yang bergerak dengan front = (front + 1) % K, sehingga O(1).

Alasan menggunakan count pada antrean melingkar: jika hanya menggunakan front dan rear, keadaan kosong dan penuh sama-sama menghasilkan front == rear sehingga tidak bisa dibedakan. Dengan count, antrean kosong jika count == 0 dan penuh jika count == K.

Ketika antrean penuh, saya memilih untuk memperbesar kapasitasnya 2 kali lipat agar pesanan tidak ditolak. Jika dequeue dilakukan saat antrean kosong, hasilnya adalah None.

| Perintah | Elemen yang digeser | Waktu |
|---|---|---|
| Dequeue naif 100x | 1.980.050 | 109 ms |
| Dequeue circular 100x | 0 | 0.08 ms |


## M3 - Sort & Search

- Insertion sort: O(n^2). Algoritma ini stabil karena elemen hanya digeser jika lebih besar (>), bukan lebih besar atau sama dengan (>=). Data lebih dari 20.000 baris ditolak karena prosesnya terlalu lama.
- Merge sort: O(n log n). Algoritma ini stabil karena saat penggabungan menggunakan <=, sehingga elemen dari bagian kiri didahulukan. Sisa elemen dari bagian kiri atau kanan juga harus disalin.
- Linear search: O(n). Data tidak perlu terurut.
- Binary search: O(log n). Data harus sudah terurut berdasarkan oid. Daftar terurut tersebut dibuat satu kali menggunakan merge sort.

Jumlah perbandingan (diurutkan berdasarkan harga):

| n | Insertion sort | Merge sort |
|---|---|---|
| 1000 | 233.802 | 8.650 |
| 2000 | 962.430 | 19.240 |
| 4000 | 3.831.520 | 42.355 |

Ketika n dikali 2, jumlah perbandingan insertion sort naik sekitar 4 kali, sedangkan merge sort hanya naik sekitar 2 kali. Hasil ini sesuai dengan kompleksitas O(n^2) dan O(n log n).
Merge sort untuk 200.000 data membutuhkan waktu sekitar 1 detik.

Pencarian O-137442:
- Linear search: 137.442 perbandingan.
- Binary search: 17 perbandingan. Namun, daftar terurutnya perlu dibuat terlebih dahulu (sekitar 680 ms), sehingga binary search baru lebih menguntungkan jika pencarian dilakukan berkali-kali.
