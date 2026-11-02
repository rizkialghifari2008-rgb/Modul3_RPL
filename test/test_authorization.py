from unittest.mock import MagicMock, patch
from controllers.buku_controller import BukuController

def test_otorisasi_role_anggota():
    with patch('controllers.buku_controller.BukuView') as mock_view_cls, \
         patch('controllers.buku_controller.BukuModel') as mock_model_cls:
        mock_view = MagicMock()
        mock_view_cls.return_value = mock_view

        ctrl = BukuController(user_role='anggota')

        # Tombol Update dan Delete harus dikonfigurasi terkunci (disabled) untuk role anggota
        mock_view.btn_update.configure.assert_called_with(state='disabled')
        mock_view.btn_delete.configure.assert_called_with(state='disabled')
        mock_view.btn_simpan.configure.assert_called_with(state='disabled', text='Akses Terkunci (Khusus Admin)')

def test_otorisasi_role_admin():
    with patch('controllers.buku_controller.BukuView') as mock_view_cls, \
         patch('controllers.buku_controller.BukuModel') as mock_model_cls:
        mock_view = MagicMock()
        mock_view_cls.return_value = mock_view

        ctrl = BukuController(user_role='admin')

        # Untuk admin, configure state='disabled' TIDAK boleh dipanggil
        for call in mock_view.btn_update.configure.call_args_list:
            assert call.kwargs.get('state') != 'disabled'
        for call in mock_view.btn_delete.configure.call_args_list:
            assert call.kwargs.get('state') != 'disabled'

def test_logout_action():
    with patch('controllers.buku_controller.BukuView') as mock_view_cls, \
         patch('controllers.buku_controller.BukuModel') as mock_model_cls:
        mock_view = MagicMock()
        mock_view_cls.return_value = mock_view

        ctrl = BukuController(user_role='anggota')

        with patch('controllers.auth_controller.AuthController') as mock_auth_cls:
            mock_auth = MagicMock()
            mock_auth_cls.return_value = mock_auth

            ctrl.logout()

            # Memverifikasi jendela perpustakaan ditutup
            mock_view.destroy.assert_called_once()
            # Memverifikasi AuthController dipanggil dan dijalankan untuk membuka LoginView
            mock_auth_cls.assert_called_once()
            mock_auth.run.assert_called_once()
