import math

# Petunjuk penulisan fungsi
print("\nMETODE SECANT")
print("=" * 14)
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

# Format angka agar 6 digit desimal, tanpa trailing zero, tanpa notasi ilmiah
def format_angka(angka):
    if abs(angka) < 1e-15:
        return '0.000000'
    return format(angka, '.6f').rstrip('0').rstrip('.')

# Input epsilon dan dua tebakan awal x0, x1
epsilon = float(input("Masukkan nilai epsilon: "))
x0 = float(input("Masukkan nilai awal x0: "))
x1 = float(input("Masukkan nilai awal x1: "))

# Tabel iterasi
print("\nHasil Iterasi Secant:")
print("-" * 108)
print(f"{'Iterasi':<10}| {'x0':<15}| {'x1':<15}| {'f(x0)':<15}| {'f(x1)':<15}| {'x2':<15}| {'f(x2)':<15}")
print("-" * 108)

iterasi = 1

while True:
    fx0 = f(x0)
    fx1 = f(x1)

    if fx1 - fx0 == 0:
        print("Pembagian dengan nol terjadi. Iterasi dihentikan.")
        break

    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
    fx2 = f(x2)

    print(f"{iterasi:<10}| {format_angka(x0):<15}| {format_angka(x1):<15}| {format_angka(fx0):<15}| {format_angka(fx1):<15}| {format_angka(x2):<15}| {format_angka(fx2):<15}")

    if abs(fx2) <= epsilon:
        print("-" * 108)
        print(f"\n|f(x2)| = {format_angka(abs(fx2))}  ≤ epsilon = {format_angka(epsilon)}, proses dihentikan.")
        print(f"Jadi, salah satu akar dari persamaan tersebut adalah x2 = {format_angka(x2)}")
        break

    # Perbarui x0 dan x1
    x0, x1 = x1, x2
    iterasi += 1
