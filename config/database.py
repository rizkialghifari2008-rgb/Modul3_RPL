import os
import traceback
import mysql.connector
from mysql.connector import Error

# Import plugin autentikasi & locales agar PyInstaller menyertakannya saat dijadikan .exe
try:
    import mysql.connector.plugins.mysql_native_password
    import mysql.connector.plugins.caching_sha2_password
    import mysql.connector.plugins.sha256_password
    import mysql.connector.plugins.mysql_clear_password
    import mysql.connector.locales.eng.client_error
except ImportError:
    pass

class Database:
    last_error = ""

    def __init__(self):
        # Menggunakan 127.0.0.1 untuk mencegah masalah resolusi IPv6 (::1) pada Windows 11
        self.host = "127.0.0.1"
        self.db_name = "perpustakaan"
        self.username = "root"
        self.password = ""
        self.port = 3306
        self.conn = None

    def get_connection(self):
        Database.last_error = ""
        try:
            # Gunakan kembali koneksi jika masih aktif
            if self.conn and self.conn.is_connected():
                return self.conn

            # 1. Coba koneksi ke 127.0.0.1 (IPv4 standar Laragon)
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    database=self.db_name,
                    user=self.username,
                    password=self.password
                )
            except Exception as e1:
                # 2. Coba fallback ke localhost
                try:
                    self.conn = mysql.connector.connect(
                        host="localhost",
                        port=self.port,
                        database=self.db_name,
                        user=self.username,
                        password=self.password
                    )
                except Exception as e2:
                    # 3. Coba fallback menggunakan pure Python protocol (kebal missing C-DLL)
                    try:
                        self.conn = mysql.connector.connect(
                            host=self.host,
                            port=self.port,
                            database=self.db_name,
                            user=self.username,
                            password=self.password,
                            use_pure=True
                        )
                    except Exception as e3:
                        raise e1

            if self.conn and self.conn.is_connected():
                return self.conn
        except Exception as e:
            err_msg = f"{type(e).__name__}: {e}"
            Database.last_error = err_msg
            print(f"Koneksi Gagal: {err_msg}")
            try:
                log_path = os.path.join(os.getcwd(), "koneksi_error.log")
                with open(log_path, "a") as f:
                    f.write(f"\n--- {traceback.format_exc()} ---\n")
            except Exception:
                pass
            return None
        return None
