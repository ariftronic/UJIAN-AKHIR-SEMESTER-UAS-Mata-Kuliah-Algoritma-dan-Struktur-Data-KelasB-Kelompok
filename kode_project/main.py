# ============================================================
#  main.py
#  Ditulis oleh: Anggota 1 (Ketua) - integrasi & menu CLI
#  SISTEM ANTREAN & MANAJEMEN PASIEN RUMAH SAKIT
# ============================================================
from Arif_1 import Patient, Queue, Stack, Aksi, PRIORITAS_LABEL
from anggota2 import BST
from anggota3 import BinaryHeap


class RumahSakitSystem:
    def __init__(self):
        self.antrean = Queue()        # pendaftaran (FIFO)
        self.rekam_medis = BST()      # data pasien (by RM)
        self.triase = BinaryHeap()    # prioritas (max-heap)
        self.riwayat = Stack()        # riwayat/undo (LIFO)
        self.no_rm = 1000             # generator nomor RM
        self._contoh_loaded = False   # guard isi_contoh

    def daftar_pasien(self):
        nama = input("Nama pasien           : ").strip()
        if not nama:
            print(">> Nama tidak boleh kosong.")
            return
        prioritas = self._input_prioritas()
        if prioritas is None:
            return
        self.no_rm += 1
        pasien = Patient(self.no_rm, nama, prioritas)
        self.antrean.enqueue(pasien)
        self.riwayat.push(Aksi("DAFTAR", f"Daftar: {pasien.nama} (RM{pasien.rm})", pasien))
        print(f">> {pasien.nama} masuk antrean pendaftaran (RM{pasien.rm}).")

    def registrasi_pasien(self):
        pasien = self.antrean.dequeue()
        if pasien is None:
            print(">> Antrean pendaftaran kosong.")
            return
        self.rekam_medis.insert(pasien)
        self.triase.insert(pasien)
        self.riwayat.push(Aksi("REGISTRASI",
                               f"Registrasi: {pasien.nama} (RM{pasien.rm})", pasien))
        print(f">> {pasien.nama} diregistrasi ke rekam medis & masuk antrean triase.")

    def panggil_pasien(self):
        pasien = self.triase.delete_root()
        if pasien is None:
            print(">> Tidak ada pasien di antrean triase.")
            return
        self.riwayat.push(Aksi("PANGGIL",
                               f"Panggil: {pasien.nama} (RM{pasien.rm})", pasien))
        print(f">> Memanggil {pasien.nama} "
              f"[{PRIORITAS_LABEL[pasien.prioritas]}] untuk pemeriksaan.")

    def cari_pasien(self):
        rm = self._input_int("Masukkan Nomor RM : ")
        if rm is None:
            return
        pasien = self.rekam_medis.search(rm)
        print(f">> Ditemukan: {pasien}" if pasien else ">> Data tidak ditemukan.")

    def hapus_pasien(self):
        rm = self._input_int("Masukkan Nomor RM : ")
        if rm is None:
            return
        pasien = self.rekam_medis.search(rm)
        if pasien is None:
            print(">> Data tidak ditemukan.")
            return
        in_heap = self.triase.contains(rm)
        self.rekam_medis.delete(rm)
        self.triase.remove_by_rm(rm)
        self.riwayat.push(Aksi("HAPUS",
                               f"Hapus: {pasien.nama} (RM{pasien.rm})", pasien, in_heap))
        print(f">> Data {pasien.nama} dihapus dari rekam medis.")

    def daftar_terurut(self):
        pasien_list = self.rekam_medis.inorder()
        if not pasien_list:
            print("   (rekam medis kosong)")
            return
        print("   Daftar pasien terurut (Inorder by RM):")
        for p in pasien_list:
            print(f"   - {p}")
        print(f"   Tinggi tree   : {self.rekam_medis.height()}")
        print(f"   Jumlah node   : {self.rekam_medis.count()}")

    def lihat_antrean(self):
        print("   Antrean pendaftaran (depan -> belakang):")
        self.antrean.display()
        depan = self.antrean.peek()
        if depan:
            print(f"   Paling depan : {depan}")

    def lihat_triase(self):
        print("   Antrean triase (heap):")
        self.triase.display()
        top = self.triase.peek()
        if top:
            print(f"   Prioritas tertinggi : {top}")

    def lihat_riwayat(self):
        print("   Riwayat aksi (terbaru -> terlama):")
        self.riwayat.display()

    def undo(self):
        aksi = self.riwayat.pop()
        if aksi is None:
            print(">> Tidak ada aksi untuk di-undo.")
            return
        if aksi.jenis == "DAFTAR":
            self.antrean.remove_by_rm(aksi.patient.rm)
            print(f">> Undo daftar: {aksi.patient.nama} "
                  f"dikeluarkan dari antrean pendaftaran.")
        elif aksi.jenis == "REGISTRASI":
            self.rekam_medis.delete(aksi.patient.rm)
            self.triase.remove_by_rm(aksi.patient.rm)
            self.antrean.enqueue_front(aksi.patient)
            print(f">> Undo registrasi: {aksi.patient.nama} "
                  f"dikembalikan ke antrean pendaftaran.")
        elif aksi.jenis == "PANGGIL":
            self.triase.insert(aksi.patient)
            print(f">> Undo panggil: {aksi.patient.nama} kembali ke antrean triase.")
        elif aksi.jenis == "HAPUS":
            self.rekam_medis.insert(aksi.patient)
            if aksi.in_heap:
                self.triase.insert(aksi.patient)
            print(f">> Undo hapus: data {aksi.patient.nama} dikembalikan.")

    def isi_contoh(self):
        if self._contoh_loaded:
            print(">> Data contoh sudah pernah dimuat.")
            return
        contoh = [("Andi", 3), ("Budi", 5), ("Citra", 1), ("Dewi", 4), ("Eka", 2)]
        for nama, pr in contoh:
            self.no_rm += 1
            p = Patient(self.no_rm, nama, pr)
            self.rekam_medis.insert(p)
            self.triase.insert(p)
            self.riwayat.push(Aksi("REGISTRASI", f"Registrasi: {p.nama} (RM{p.rm})", p))
        self._contoh_loaded = True
        print(">> 5 data contoh berhasil dimuat ke rekam medis dan triase.")

    def _input_int(self, prompt):
        try:
            return int(input(prompt).strip())
        except ValueError:
            print(">> Input harus berupa angka.")
            return None

    def _input_prioritas(self):
        print("   Skor prioritas: 5=Darurat 4=Mendesak 3=Prioritas 2=Ringan 1=Rutin")
        pr = self._input_int("Skor prioritas (1-5)  : ")
        if pr is None:
            return None
        if pr < 1 or pr > 5:
            print(">> Skor harus 1 sampai 5.")
            return None
        return pr


def main():
    sistem = RumahSakitSystem()
    menu = """
============================================================
     SISTEM ANTREAN & MANAJEMEN PASIEN RUMAH SAKIT
============================================================
 1.  Daftar pasien baru            (Queue: enqueue)
 2.  Registrasi pasien dari antrean (Queue->BST->Heap)
 3.  Panggil pasien prioritas       (Heap: delete root)
 4.  Cari data pasien               (BST: search)
 5.  Hapus data pasien              (BST: delete)
 6.  Daftar pasien terurut          (BST: inorder+height+count)
 7.  Lihat antrean pendaftaran      (Queue: display)
 8.  Lihat antrean triase           (Heap: display)
 9.  Lihat riwayat aksi             (Stack: display)
 10. Undo aksi terakhir             (Stack: pop)
 11. Isi data contoh (demo)
 0.  Keluar
============================================================"""
    aksi = {
        "1": sistem.daftar_pasien,
        "2": sistem.registrasi_pasien,
        "3": sistem.panggil_pasien,
        "4": sistem.cari_pasien,
        "5": sistem.hapus_pasien,
        "6": sistem.daftar_terurut,
        "7": sistem.lihat_antrean,
        "8": sistem.lihat_triase,
        "9": sistem.lihat_riwayat,
        "10": sistem.undo,
        "11": sistem.isi_contoh,
    }
    while True:
        print(menu)
        pilih = input("Pilih menu : ").strip()
        if pilih == "0":
            print(">> Terima kasih. Program selesai.")
            break
        fn = aksi.get(pilih)
        if fn is None:
            print(">> Menu tidak valid.")
        else:
            print("-" * 60)
            fn()


if __name__ == "__main__":
    main()