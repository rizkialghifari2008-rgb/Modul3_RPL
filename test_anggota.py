from models.anggota_model import AnggotaModel

model = AnggotaModel()

# 1. Menguji fungsi Create (menambah data anggota baru)
print("Menambahkan data anggota...")
model.create_anggota("Budi Santoso", "Jl. Sudirman No. 10")
print("Data anggota berhasil disimpan!")

# 2. Menguji fungsi Read (menampilkan data anggota)
print("\n=== Daftar Anggota Sebelum Update/Delete ===")
daftar_anggota = model.get_all_anggota()
for anggota in daftar_anggota:
    print(f"[{anggota['id_anggota']}] {anggota['nama']} - {anggota['alamat']}")

# 3. Menguji fungsi Update (mengubah data anggota berdasarkan id)
if daftar_anggota:
    id_terakhir = daftar_anggota[-1]['id_anggota']
    print(f"\nMengubah data anggota ID {id_terakhir}...")
    model.update_anggota(id_terakhir, "Budi Santoso (Updated)", "Jl. Thamrin No. 20")
    print("Data anggota berhasil diubah!")

    # 4. Menguji fungsi Delete (menghapus data anggota berdasarkan id)
    print(f"\nMenghapus data anggota ID {id_terakhir}...")
    model.delete_anggota(id_terakhir)
    print("Data anggota berhasil dihapus!")

# Tampilkan ulang daftar anggota setelah perubahan
print("\n=== Daftar Anggota Setelah Update & Delete ===")
daftar_anggota_terbaru = model.get_all_anggota()
for anggota in daftar_anggota_terbaru:
    print(f"[{anggota['id_anggota']}] {anggota['nama']} - {anggota['alamat']}")