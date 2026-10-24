from models.buku_model import BukuModel

model = BukuModel()

# 1. Menguji fungsi Create (menambah buku baru)
print("Menambahkan data buku...")
model.create_buku("Pemrograman Python MVC", "Guido van Rossum", 2023)
print("Data berhasil disimpan ke Laragon MySQL!")

# 2. Menguji fungsi Read (menampilkan data)
print("\n=== Daftar Buku Sebelum Update/Delete ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# 3. Menguji fungsi Update (mengubah data buku berdasarkan id, contoh id=6)
print("\nMengubah data buku...")
model.update_buku(6, "Pemrograman Python Lanjutan", "Guido van Rossum", 2024)
print("Data buku berhasil diubah!")

# 4. Menguji fungsi Delete (menghapus data buku berdasarkan id, contoh id=6)
print("\nMenghapus data buku...")
model.delete_buku(6)
print("Data buku berhasil dihapus!")

# Tampilkan ulang daftar buku setelah perubahan
print("\n=== Daftar Buku Setelah Update & Delete ===")
daftar_buku_terbaru = model.get_all_buku()
for buku in daftar_buku_terbaru:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")