# Import plugin autentikasi & locales agar PyInstaller menyertakannya ke file .exe
try:
    import mysql.connector.plugins.mysql_native_password
    import mysql.connector.plugins.caching_sha2_password
    import mysql.connector.plugins.sha256_password
    import mysql.connector.plugins.mysql_clear_password
    import mysql.connector.locales.eng.client_error
except ImportError:
    pass

from controllers.auth_controller import AuthController

if __name__ == "__main__":
    app = AuthController()
    app.run()
