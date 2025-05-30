from paddleocr import PaddleOCR
import numpy as np

# Remove use_gpu parameter because it's not recognized anymore
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Use GPU automatically if available

def preprocess_image(pil_img):
    return np.array(pil_img)

def extract_text(img):
    result = ocr.ocr(img)
    res = result[0]

    text = "\n".join(res['rec_texts'])

    data = {
        "text": res['rec_texts'],
        "conf": res['rec_scores'],
        "polygons": res['rec_polys'],
    }
    return text, data
