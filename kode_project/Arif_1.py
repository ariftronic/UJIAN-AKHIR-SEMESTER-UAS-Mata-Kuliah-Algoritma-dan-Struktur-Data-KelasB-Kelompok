# ============================================================
#  anggota1_queue_stack.py
#  Ditulis oleh: Anggota 1 (Ketua)
#  Berisi: data pasien, Node, Queue (FIFO), Stack (LIFO), Aksi
# ============================================================

# Label prioritas triase (skor tinggi = lebih gawat)
PRIORITAS_LABEL = {
    5: "Darurat",
    4: "Mendesak",
    3: "Prioritas",
    2: "Ringan",
    1: "Rutin",
}


class Patient:
    def __init__(self, rm, nama, prioritas):
        self.rm = rm                # Nomor Rekam Medis (key BST)
        self.nama = nama
        self.prioritas = prioritas  # skor 1..5 (5 = paling gawat)

    def __str__(self):
        label = PRIORITAS_LABEL.get(self.prioritas, "-")
        return f"RM{self.rm} | {self.nama} | Prioritas {self.prioritas} ({label})"


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# ------------------ QUEUE (FIFO) ------------------
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def enqueue(self, data):
        node = Node(data)
        if self.is_empty():
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def enqueue_front(self, data):
        node = Node(data)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head = node
        self.size += 1

    def remove_last(self):
        if self.is_empty():
            return None
        if self.head is self.tail:
            data = self.head.data
            self.head = self.tail = None
            self.size -= 1
            return data
        current = self.head
        while current.next is not self.tail:
            current = current.next
        data = self.tail.data
        current.next = None
        self.tail = current
        self.size -= 1
        return data

    def remove_by_rm(self, rm):
        """Hapus node dengan patient.rm tertentu dari Queue."""
        if self.is_empty():
            return None
        # Cek head
        if self.head.data.rm == rm:
            return self.dequeue()
        current = self.head
        while current.next is not None:
            if current.next.data.rm == rm:
                removed = current.next.data
                current.next = current.next.next
                if current.next is None:
                    self.tail = current
                self.size -= 1
                return removed
            current = current.next
        return None

    def dequeue(self):
        if self.is_empty():
            return None
        node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return node.data

    def peek(self):
        return None if self.is_empty() else self.head.data

    def display(self):
        if self.is_empty():
            print("   (antrean pendaftaran kosong)")
            return
        current = self.head
        i = 1
        while current is not None:
            print(f"   {i}. {current.data}")
            current = current.next
            i += 1


# ------------------ STACK (LIFO) ------------------
class Aksi:
    def __init__(self, jenis, deskripsi, patient=None, in_heap=False):
        self.jenis = jenis
        self.deskripsi = deskripsi
        self.patient = patient
        self.in_heap = in_heap

    def __str__(self):
        return self.deskripsi


class Stack:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def push(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        self.size += 1

    def pop(self):
        if self.is_empty():
            return None
        node = self.head
        self.head = self.head.next
        self.size -= 1
        return node.data

    def peek(self):
        return None if self.is_empty() else self.head.data

    def display(self):
        if self.is_empty():
            print("   (riwayat kosong)")
            return
        current = self.head
        i = 1
        while current is not None:
            print(f"   {i}. {current.data}")
            current = current.next
            i += 1