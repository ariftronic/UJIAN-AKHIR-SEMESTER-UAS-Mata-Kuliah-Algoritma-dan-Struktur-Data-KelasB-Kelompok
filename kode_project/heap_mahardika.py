class BinaryHeap:
    def __init__(self):
        self.data = []   # representasi array

    def is_empty(self):
        return len(self.data) == 0

    def peek(self):
        return None if self.is_empty() else self.data[0]

    def contains(self, rm):
        return any(p.rm == rm for p in self.data)

    def _heapify_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.data[i].prioritas > self.data[parent].prioritas:
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent
            parent = (i - 1) // 2

    def _heapify_down(self, i):
        n = len(self.data)
        while True:
            left, right, largest = 2 * i + 1, 2 * i + 2, i
            if left < n and self.data[left].prioritas > self.data[largest].prioritas:
                largest = left
            if right < n and self.data[right].prioritas > self.data[largest].prioritas:
                largest = right
            if largest == i:
                break
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest

    def insert(self, patient):
        if self.contains(patient.rm):
            return  # sudah ada, jangan duplikat
        self.data.append(patient)
        self._heapify_up(len(self.data) - 1)

    def delete_root(self):
        if self.is_empty():
            return None
        root = self.data[0]
        last = self.data.pop()
        if not self.is_empty():
            self.data[0] = last
            self._heapify_down(0)
        return root

    def remove_by_rm(self, rm):
        idx = -1
        for i, p in enumerate(self.data):
            if p.rm == rm:
                idx = i
                break
        if idx == -1:
            return None
        removed = self.data[idx]
        last = self.data.pop()
        if idx < len(self.data):
            self.data[idx] = last
            self._heapify_down(idx)
            self._heapify_up(idx)
        return removed

    def display(self):
        if self.is_empty():
            print("   (antrean triase kosong)")
            return
        for idx, p in enumerate(self.data):
            print(f"   [{idx}] {p}") 