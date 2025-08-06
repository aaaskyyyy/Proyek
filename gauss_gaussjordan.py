import numpy as np

# Fungsi untuk input matriks A dan vektor B dari user
def input_data():
    n = int(input("Masukkan ordo matriks (n): "))
    print("Masukkan elemen matriks A (baris demi baris, pisahkan dengan spasi):")
    A = []
    for i in range(n):
        row = list(map(float, input(f"A[{i+1}] = ").split()))
        A.append(row)
    A = np.array(A, dtype=float)

    print("Masukkan elemen vektor B:")
    b = []
    for i in range(n):
        val = float(input(f"B[{i+1}] = "))
        b.append(val)
    b = np.array(b, dtype=float)
    return A, b

# Fungsi untuk mencetak matriks augmented
def print_augmented_matrix(AB, title):
    print(f"\n=== {title} ===")
    for row in AB:
        formatted_row = []
        for i, val in enumerate(row):
            if val == int(val):
                formatted_row.append(f"{int(val):>6}")
            else:
                formatted_row.append(f"{val:>6.2f}")
        row_str = " ".join(formatted_row[:-1]) + " | " + formatted_row[-1]
        print(f"[ {row_str} ]")

# METODE GAUSS
def gauss_elimination(A, b):
    n = len(b)
    AB = np.hstack((A, b.reshape(-1, 1)))  # Matriks Augmented [A | b]

    # Forward Elimination
    for i in range(n):
        if AB[i][i] == 0:   # Jika pivot = 0, tukar dengan baris di bawahnya
            for k in range(i + 1, n):
                if AB[k][i] != 0:
                    AB[[i, k]] = AB[[k, i]]
                    break
        for j in range(i + 1, n):   # Hilangkan elemen di bawah pivot
            factor = AB[j][i] / AB[i][i]
            AB[j] -= factor * AB[i]

    print_augmented_matrix(AB, "Matriks Setelah Eliminasi Gauss")

    # Back Substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):  # Mulai dari baris paling bawah
        x[i] = AB[i, -1]                
        for j in range(i + 1, n):
            x[i] -= AB[i, j] * x[j]
        x[i] /= AB[i][i]

    return x

# METODE GAUSS-JORDAN
def gauss_jordan(A, b):
    n = len(b)
    AB = np.hstack((A, b.reshape(-1, 1)))   # Gabungkan A dan b menjadi matriks augmented [A | b]

    for i in range(n):
        if AB[i][i] == 0:   # Jika pivot 0, tukar baris
            for k in range(i + 1, n):
                if AB[k][i] != 0:
                    AB[[i, k]] = AB[[k, i]]
                    break
        AB[i] = AB[i] / AB[i][i]    # Normalisasi baris agar pivot = 1
        for j in range(n):
            if j != i:              # Hilangkan semua elemen di atas & bawah pivot
                factor = AB[j][i]
                AB[j] -= factor * AB[i]

    print_augmented_matrix(AB, "Matriks Setelah Eliminasi Gauss-Jordan")
    return AB[:, -1]    # Ambil kolom terakhir sebagai solusi karena bentuk sudah [I | x]

# Fungsi untuk mencetak solusi dengan variabel x, y, z
def cetak_solusi(solusi, metode):
    print(f"\n=== HASIL METODE {metode.upper()} ===")
    var_labels = ['x', 'y', 'z'] + [f"x{i+1}" for i in range(3, len(solusi))]
    for i, val in enumerate(solusi):
        print(f"{var_labels[i]} = {val:.2f}")

# MAIN PROGRAM
print("=== PROGRAM METODE GAUSS & GAUSS-JORDAN ===")
A, b = input_data()

x_gauss = gauss_elimination(A.copy(), b.copy())
x_jordan = gauss_jordan(A.copy(), b.copy())

cetak_solusi(x_gauss, "Gauss")
cetak_solusi(x_jordan, "Gauss-Jordan")
