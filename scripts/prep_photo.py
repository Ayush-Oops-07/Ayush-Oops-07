import sys, os
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

img = cv2.imread(INP)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = np.zeros(img.shape[:2], np.uint8)
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
h, w = img.shape[:2]
rect = (int(w*0.05), int(h*0.02), int(w*0.90), int(h*0.96))
cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 8, cv2.GC_INIT_WITH_RECT)
alpha = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)
alpha = cv2.GaussianBlur(alpha.astype(np.float32), (0, 0), 1.2)
alpha = np.clip(alpha, 0, 255)
clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
gray = clahe.apply(gray)
gray = cv2.convertScaleAbs(gray, alpha=1.08, beta=15)
mask_f = alpha / 255.0
out = gray.astype(np.float32) * mask_f + 255.0 * (1.0 - mask_f)
out = np.clip(out, 0, 255).astype(np.uint8)
Image.fromarray(out, mode="L").save(OUT)
print("wrote", OUT, out.shape)
