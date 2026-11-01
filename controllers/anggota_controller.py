import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        # Inisialisasi Model dan View Anggota
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Binding tombol simpan di View Anggota (hanya fitur tambah data)
        self.view.btn_simpan.configure(command=self.simpan_data)

        # Memuat data ke tabel anggota saat pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Kosongkan tabel sebelum memuat ulang
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Ambil seluruh data anggota dari database
        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        # Validasi Form Kosong
        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        # Mengirim data ke Model untuk disimpan (Tambah Data)
        berhasil = self.model.create_anggota(nama, alamat)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            # Bersihkan form input setelah berhasil menambah data
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
            # Muat ulang tabel agar data baru langsung muncul
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    app = AnggotaController()
    app.run()