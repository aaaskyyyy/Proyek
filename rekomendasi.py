import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# === NLP Tools ===
stemmer = StemmerFactory().create_stemmer()
stop_factory = StopWordRemoverFactory()
stopwords = stop_factory.get_stop_words()

kamus_normal = {
    'murmer': 'murah', 'gaje': 'tidak jelas', 'ga': 'tidak',
    'nggak': 'tidak', 'hp': 'handphone', 'bln': 'bulan'
}

def normalisasi(teks):
    return ' '.join([kamus_normal.get(k, k) for k in teks.split()])

def preprocess(teks):
    teks = re.sub(r'[^\w\s]', ' ', teks.lower())
    teks = re.sub(r'\d+', '', teks)
    teks = re.sub(r'\s+', ' ', teks)
    teks = normalisasi(teks)
    tokens = teks.split()
    tokens = [t for t in tokens if t not in stopwords]
    return ' '.join([stemmer.stem(t) for t in tokens])

# === Daftar Kategori ===
kategori_list = [
    "alat musik", "perlengkapan bayi", "buku", "elektronik", "kebutuhan hewan peliharaan",
    "kendaraan", "kesehatan", "kecantikan", "tas", "hiburan", "pakaian", "perabotan",
    "alat olahraga", "perhiasan", "alat renovasi", "jual rumah", "taman", "lainnya"
]

# === Tampilkan Daftar Kategori dalam 3 Kolom ===
print("\n📦 PILIHAN KATEGORI PRODUK:")
kolom = 3
baris = (len(kategori_list) + kolom - 1) // kolom
for i in range(baris):
    baris_kolom = []
    for j in range(kolom):
        idx = i + j * baris
        if idx < len(kategori_list):
            nomor = idx + 1
            nama = kategori_list[idx].capitalize()
            baris_kolom.append(f"{nomor:>2}. {nama:<27}")
    print("   ".join(baris_kolom))

# === Input dari Pengguna ===
try:
    pilihan = int(input("\nMasukkan nomor kategori (1–18): "))
    if not 1 <= pilihan <= len(kategori_list):
        raise ValueError
except ValueError:
    print("❌ Input tidak valid. Masukkan angka 1–18.")
    exit()

kategori_input = kategori_list[pilihan - 1]
deskripsi = input("Deskripsi produk: ")

# === Preprocess input ===
gabungan_input = f"{kategori_input} {deskripsi}"
preprocessed_input = preprocess(gabungan_input)
tokens_input = preprocessed_input.split()

# === Baca file Excel dan sheet ===
file_path = "judul_per_kategori_terklasifikasi.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = [s.lower() for s in xls.sheet_names]

if kategori_input.lower() not in sheet_names:
    print(f"⚠️ Sheet '{kategori_input}' tidak ditemukan. Menggunakan sheet 'lainnya'...")
    if "lainnya" not in sheet_names:
        raise ValueError("❌ Sheet 'lainnya' juga tidak ditemukan.")
    kategori_input = "lainnya"

# Baca sheet
df = pd.read_excel(xls, sheet_name=kategori_input.lower())

# Ambil kolom skor tf-idf
tfidf_df = df.drop(columns=[col for col in df.columns if col.lower().startswith("judul") or col.lower() == "kategori"])
mean_tfidf = tfidf_df.mean()

# Skor dari kata input
kata_skor = {kata: mean_tfidf.get(kata, 0) for kata in tokens_input if kata in mean_tfidf}
top_kata = sorted(kata_skor.items(), key=lambda x: x[1], reverse=True)[:3]
top_words = [kata for kata, _ in top_kata]

while len(top_words) < 3:
    top_words.append("produk")

# === Buat Judul Lebih Natural ===
judul1 = f"{top_words[0].capitalize()} {top_words[1]} {top_words[2]}"
judul2 = f"{top_words[0].capitalize()} {top_words[2]} terbaik untuk kamu"
judul3 = f"Rekomendasi {kategori_input.lower()}: {top_words[0].capitalize()} {top_words[1]}"

# === Generator Tagar ===
all_tfidf_words = mean_tfidf.sort_values(ascending=False).head(10).index.tolist()
input_tags = [f"#{kata}" for kata in top_words if kata in mean_tfidf.index]
kategori_tags = [f"#{kata}" for kata in all_tfidf_words if kata not in top_words][:5]

# Gabungkan semua tagar
tagar_final = input_tags + kategori_tags

# === Output ===
print("\n✅ Rekomendasi Judul SEO-Friendly:")
print("1.", judul1)
print("2.", judul2)
print("3.", judul3)

print("\n🔎 Kata penting dari deskripsi:")
for i, (kata, skor) in enumerate(top_kata, 1):
    print(f"{i}. {kata} → skor: {round(skor, 4)}")

print("\n🏷️ Rekomendasi Tagar (Hashtag):")
print(" ".join(tagar_final))
