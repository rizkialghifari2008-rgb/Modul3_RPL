import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        # Inisialisasi Role, Model, dan View
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_delete.configure(command=self.hapus_data)

        # Binding event klik baris pada tabel untuk mengisi form secara otomatis
        self.view.tabel.bind("<<TreeviewSelect>>", self.on_tabel_klik)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol aksi
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_delete.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def on_tabel_klik(self, event=None):
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_values = self.view.tabel.item(selected_item, 'values')
            if item_values and len(item_values) >= 4:
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_judul.insert(0, item_values[1])
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_penulis.insert(0, item_values[2])
                self.view.entry_tahun.delete(0, 'end')
                self.view.entry_tahun.insert(0, item_values[3])

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data dari Model (database)
        data_buku = self.model.get_all_buku()

        # Memasukkan data baru ke dalam tabel View
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def simpan_data(self):
        # Proteksi ganda di Level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def hapus_data(self):
        # Proteksi ganda di Level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        # Mendapatkan item yang dipilih di tabel
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus!")
            return

        # Mengambil ID buku dari item yang dipilih
        item_values = self.view.tabel.item(selected_item, 'values')
        id_buku = item_values[0]

        # Konfirmasi penghapusan
        konfirmasi = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus buku dengan ID {id_buku}?")
        if konfirmasi:
            berhasil = self.model.delete_buku(id_buku)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                # Bersihkan form input
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_tahun.delete(0, 'end')
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def perbarui_data(self):
        # Proteksi ganda di Level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        # Mendapatkan item yang dipilih di tabel
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui!")
            return

        # Mengambil ID buku dari item yang dipilih
        item_values = self.view.tabel.item(selected_item, 'values')
        id_buku = item_values[0]

        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke Model untuk diperbarui
        berhasil = self.model.update_buku(id_buku, judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            # Muat ulang tabel agar data terbaru muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()