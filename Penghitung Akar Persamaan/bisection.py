import math

print("\nMETODE BISECTION")
print("=" * 18)
print("Aturan memasukkan persamaan (f(x)):")
print("1. Gunakan tanda  untuk pangkat, bukan ^. Contoh: x^3 tulis sebagai x**3.")
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

persamaan = input("\nMasukkan persamaan (f(x)): ")

def f(x):
    return eval(persamaan, {"x": x, "math": math})

epsilon = float(input("Masukkan nilai epsilon: "))
Xn = float(input("Masukkan nilai Xn (batas bawah): "))
Xn1 = float(input("Masukkan nilai Xn+1 (batas atas): "))

def format_angka(x):
    # Format angka tanpa notasi ilmiah, 6 digit setelah koma maksimal, dan tanpa trailing nol
    if x == int(x):
        return str(int(x))
    else:
        return f"{x:.6f}".rstrip('0').rstrip('.')

print("\n" + "-" * 110)
print("{:<10} {:<10} {:<10} {:<12} {:<12} {:<12} {:<12} {}".format(
    "Iterasi", "Xn", "Xn+1", "Xt", "f(Xn)", "f(Xn+1)", "f(Xt)", "f(Xn)*f(Xt)"
))
print("-" * 110)

iterasi = 1

while True:
    fXn = f(Xn)
    fXn1 = f(Xn1)

    Xt = (Xn + Xn1) / 2
    fXt = f(Xt)
    hasil_kali = fXn * fXt

    print("{:<10} {:<10} {:<10} {:<12} {:<12} {:<12} {:<12} {}".format(
        iterasi,
        format_angka(Xn),
        format_angka(Xn1),
        format_angka(Xt),
        format_angka(fXn),
        format_angka(fXn1),
        format_angka(fXt),
        format_angka(hasil_kali)
    ))

    if abs(fXt) <= epsilon:
        print("\n|f(Xt)| = {} ≤ epsilon = {}, proses dihentikan.".format(
            format_angka(abs(fXt)), format_angka(epsilon)))
        print("Jadi, salah satu akar dari persamaan tersebut adalah {}".format(format_angka(Xt)))
        break


    if hasil_kali < 0:
        Xn1 = Xt
    else:
        Xn = Xt

    iterasi += 1
