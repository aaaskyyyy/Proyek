import math

# Petunjuk penulisan fungsi
print("\nMETODE NEWTON")
print("=" * 13)
print("Aturan memasukkan persamaan (f(x)):")
print("1. Gunakan tanda ** untuk pangkat, bukan ^. Contoh: x^3 tulis sebagai x**3.")
print("2. Kalikan variabel dengan angka menggunakan tanda *. Contoh: 3x tulis sebagai 3*x.")
print("3. Gunakan fungsi dari modul math untuk fungsi matematika seperti:")
print("   math.exp(x) untuk e^x")
print("   math.log(x) untuk ln(x) (logaritma natural)")
print("   math.log10(x) untuk logaritma basis 10")
print("   math.sqrt(x) untuk akar kuadrat")
print("   math.sin(x), math.cos(x), math.tan(x) untuk fungsi trigonometri")
print("4. Contoh penulisan yang benar:")
print("   x**3 + x**2 - 3*x - 3         x*math.exp(x) - 1")
print("   math.cos(x) - x               x**2 - 2")
print("5. Jangan gunakan simbol seperti ^, √, atau π langsung. Gantilah dengan bentuk Python:")
print("   √x → math.sqrt(x)             π → math.pi")

# Input fungsi dari user
fx_input = input("\nMasukkan fungsi f(x): ")

# Fungsi f(x)
def f(x):
    return eval(fx_input, {"x": x, "math": math})

# Hitung turunan f'(x) secara numerik
def f_prime(x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)

# Format khusus: maksimal 6 angka di belakang koma, tanpa trailing nol, tanpa notasi ilmiah
def custom_format(val):
    if val == 0:
        return "0"
    formatted = f"{val:.6f}".rstrip('0').rstrip('.')
    return formatted

# Input epsilon dan tebakan awal x1
epsilon = float(input("Masukkan nilai epsilon: "))
x1 = float(input("Masukkan nilai awal x1: "))

# Tabel iterasi
print("\nHasil Iterasi Newton:")
print("-" * 72)
print(f"{'Iterasi':<10}| {'x1':<15}| {'f(x1)':<15}| {'x2':<15}| {'f(x2)':<15}")
print("-" * 72)

iterasi = 1

while True:
    fx1 = f(x1)
    fpx1 = f_prime(x1)

    if fpx1 == 0:
        print("Turunan = 0. Tidak bisa melanjutkan iterasi.")
        break

    x2 = x1 - (fx1 / fpx1)
    fx2 = f(x2)

    print(f"{iterasi:<10}| {custom_format(x1):<15}| {custom_format(fx1):<15}| {custom_format(x2):<15}| {custom_format(fx2):<15}")
    
    if abs(fx2) < epsilon:
        print("-" * 72)
        print(f"\n|f(x2)| = {custom_format(abs(fx2))}  ≤ epsilon = {custom_format(epsilon)}, proses dihentikan.")
        print(f"Jadi, salah satu akar dari persamaan tersebut adalah x2 = {custom_format(x2)}\n")
        break

    x1 = x2
    iterasi += 1
