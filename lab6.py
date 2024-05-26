import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Розміри матриць
n, m, k = 5, 4, 8

# Ініціалізація матриць
A = [[random.randint(1, 7) for _ in range(m)] for _ in range(n)]
B = [[random.randint(1, 20) for _ in range(k)] for _ in range(m)]
C = [[0] * k for _ in range(n)]

# Вивід матриць
print("Matrix A:")
for row in A:
    print(row)

print("\nMatrix B:")
for row in B:
    print(row)

# Мьютекс для синхронізації виводу
io_lock = threading.Lock()

# Функція для множення рядка на стовпець
def multiply_row_by_column(row, col):
    result = sum(A[row][i] * B[i][col] for i in range(m))
    with io_lock:
        print(f"[{row}, {col}] = {result}")
    C[row][col] = result

# Функція для паралельного множення матриць
def matrix_multiply(num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(n):
            for j in range(k):
                executor.submit(multiply_row_by_column, i, j)

# 1.1 Продемонструвати паралелізм обчислень
print("Matrix multiplication with parallelism:")
matrix_multiply(n * k)

# 1.2 Дослідити швидкодію множення залежно від кількості потоків
def measure_performance():
    for num_threads in range(1, n * k + 1):
        start_time = time.time()
        matrix_multiply(num_threads)
        elapsed_time = time.time() - start_time
        print(f"Threads: {num_threads} - Elapsed time: {elapsed_time:.2f} seconds")

print("\nPerformance analysis:")
measure_performance()

# 2. Змоделювати паралельну роботу зі спільною змінною
shared_variable = 0
shared_variable_lock = threading.Lock()
atomic_variable = 0

# 2.1 З використанням критичного сегменту
def increase_with_lock():
    global shared_variable
    for _ in range(10**6):
        with shared_variable_lock:
            shared_variable += 1

# 2.1 Без використання критичного сегменту
def increase_without_lock():
    global shared_variable
    for _ in range(10**6):
        shared_variable += 1

# 2.3 Повністю синхронне додавання
def increase_synchronously(counter):
    global shared_variable
    while True:
        with shared_variable_lock:
            if counter.value >= 1000:
                break
            counter.value += 1
            shared_variable += 1
            print(f"Thread {threading.current_thread().name} - Shared Variable: {shared_variable}")

class Counter:
    def __init__(self):
        self.value = 0

print("\nShared variable tests:")

# 2.1 З використанням критичного сегменту
shared_variable = 0
threads = [threading.Thread(target=increase_with_lock) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"With lock: {shared_variable}")

# 2.1 Без використання критичного сегменту
shared_variable = 0
threads = [threading.Thread(target=increase_without_lock) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"Without lock: {shared_variable}")

# 2.3 Повністю синхронне додавання
shared_variable = 0
counter = Counter()
threads = [threading.Thread(target=increase_synchronously, args=(counter,)) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"Synchronously: {shared_variable}")
