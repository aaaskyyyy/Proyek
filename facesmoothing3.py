import cv2
import numpy as np
import mediapipe as mp

# Inisialisasi Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

# Baca gambar
image = cv2.imread("coba2.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
h, w, _ = image.shape

# Deteksi landmark wajah
results = face_mesh.process(image_rgb)
mask = np.zeros((h, w), dtype=np.uint8)

# Index landmark untuk area mata dan bibir
mata_bibir_index = list(range(33, 68)) + list(range(61, 88)) + list(range(89, 93)) + list(range(95, 133)) + list(range(362, 397)) + list(range(263, 296)) + list(range(308, 324))

if results.multi_face_landmarks:
    # Simpan deteksi landmark di atas gambar
    image_landmark = image.copy()
    for face_landmarks in results.multi_face_landmarks:
        for lm in face_landmarks.landmark:
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(image_landmark, (x, y), 5, (0, 255, 0), -1)  # titik hijau

    for face_landmarks in results.multi_face_landmarks:
        for idx in mata_bibir_index:
            lm = face_landmarks.landmark[idx]
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(mask, (x, y), 5, 255, -1)

    mask = cv2.dilate(mask, np.ones((15, 15), np.uint8), iterations=1)
    mask_inv = cv2.bitwise_not(mask)

    # ==================== PENGHALUSAN ====================
    blur = cv2.bilateralFilter(image, 9, 75, 75)
    glow = cv2.GaussianBlur(blur, (0, 0), sigmaX=5)
    glowing_skin = cv2.addWeighted(blur, 0.7, glow, 0.3, 0)

    # ==================== DETEKSI NODA ====================
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    cr = ycrcb[:, :, 1]
    _, blemish_mask = cv2.threshold(cr, 150, 255, cv2.THRESH_BINARY_INV)
    blemish_mask = cv2.medianBlur(blemish_mask, 5)

    contours, _ = cv2.findContours(blemish_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    jerawat_mask = np.zeros((h, w), dtype=np.uint8)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 8 < area < 1000:
            noda=cv2.drawContours(jerawat_mask, [cnt], -1, 255, -1)

    # ==================== INPAINTING ====================
    kulit_bersih = cv2.inpaint(glowing_skin, jerawat_mask, inpaintRadius=6, flags=cv2.INPAINT_TELEA)

    # ==================== PENGGABUNGAN ====================
    tajam = cv2.bitwise_and(image, image, mask=mask)
    halus = cv2.bitwise_and(kulit_bersih, kulit_bersih, mask=mask_inv)
    hasil_akhir = cv2.add(tajam, halus)

    # Tampilkan dan simpan hasil akhir
    cv2.imshow("Kulit Halus & Bersih", hasil_akhir)
    cv2.imwrite("metode_a.jpg", hasil_akhir)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Wajah tidak terdeteksi.")
