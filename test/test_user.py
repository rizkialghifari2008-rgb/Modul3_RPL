import hashlib
from unittest.mock import MagicMock
from models.user_model import UserModel

def test_hash_password():
    password = "password123"
    expected = hashlib.sha256(password.encode('utf-8')).hexdigest()
    assert UserModel.hash_password(password) == expected

def test_register_user_berhasil():
    model = UserModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    username = "budi"
    password = "password123"
    role = "anggota"
    expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    hasil = model.register_user(username, password, role)

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    query_called, params_called = mock_cursor.execute.call_args[0]
    assert "INSERT INTO users" in query_called
    assert params_called == (username, expected_hash, role)
    model.conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_autentikasi_berhasil():
    model = UserModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    expected_user = {'id_user': 1, 'username': 'admin', 'role': 'admin'}
    mock_cursor.fetchone.return_value = expected_user

    hasil = model.autentikasi("admin", "admin123")
    assert hasil == expected_user
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()

