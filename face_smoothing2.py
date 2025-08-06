import cv2
import numpy as np

# Baca gambar wajah
image = cv2.imread("coba3.jpg")

# Pastikan gambar berhasil dibaca
if image is None:
    print("Gambar tidak ditemukan.")
    exit()

# ====== 1. EDGE-PRESERVING FILTER ======
halus = cv2.edgePreservingFilter(image, flags=1, sigma_s=60, sigma_r=0.4)

# ====== 2. DETAIL ENHANCEMENT ======
hasil_akhir = cv2.detailEnhance(halus, sigma_s=10, sigma_r=0.15)

# ================== TAMPILKAN HASIL ==================
cv2.imshow("Wajah Halus & Cerah (Cepat)", hasil_akhir)
cv2.imwrite("metode_b.jpg", hasil_akhir)
cv2.waitKey(0)
cv2.destroyAllWindows()
