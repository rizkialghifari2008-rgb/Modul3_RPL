from models.anggota_model import AnggotaModel

model = AnggotaModel()

# 1. Menguji fungsi Create (menambah anggota baru)
print("Menambahkan data anggota...")
model.create_anggota("Budi Santoso", "Jl. Sudirman No. 10")
print("Data anggota berhasil disimpan!")

# 2. Menguji fungsi Read (menampilkan data anggota)
print("\n=== Daftar Anggota ===")
daftar_anggota = model.get_all_anggota()
for anggota in daftar_anggota:
    print(f"[{anggota['id_anggota']}] {anggota['nama']} - {anggota['alamat']}")