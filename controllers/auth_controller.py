import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController
from config.database import Database

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        # Cek ketersediaan koneksi database
        if not self.model.conn or not self.model.conn.is_connected():
            self.model.conn = self.model.db.get_connection()

        if not self.model.conn or not self.model.conn.is_connected():
            err_detail = f"\n\nDetail: {Database.last_error}" if Database.last_error else ""
            messagebox.showerror(
                "Koneksi Database Gagal",
                f"Gagal terhubung ke database MySQL!{err_detail}\n\n"
                "Pastikan MySQL di Laragon / XAMPP sudah aktif (running)."
            )
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['username']} ({user['role']})!")
            # Tutup jendela Login
            self.view.destroy()
            # Buka jendela Utama Perpustakaan dengan mengirimkan role pengguna
            app_utama = BukuController(user_role=user['role'])
            app_utama.run()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def run(self):
        self.view.mainloop()
