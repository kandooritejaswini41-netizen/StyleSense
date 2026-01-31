from flask import Flask, render_template, request
import os
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------- SKIN TONE DETECTION (SIMPLE) --------
def detect_skin_tone(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    avg_color = np.mean(img.reshape(-1, 3), axis=0)
    r, g, b = avg_color

    if r > 200 and g > 180:
        return "Fair"
    elif r > 160:
        return "Medium"
    elif r > 120:
        return "Olive"
    else:
        return "Deep"

# -------- AI STYLING (SIMULATED) --------
def get_style_recommendation(skin_tone, gender):
    styles = {
        "Fair": "Pastel colors, light blue, pink, beige",
        "Medium": "Earth tones, navy blue, maroon",
        "Olive": "Green shades, brown, cream",
        "Deep": "Bright colors, white, yellow, red"
    }

    return {
        "outfit": styles[skin_tone],
        "accessories": "Minimal accessories, clean design",
        "shopping": {
            "Amazon": "https://www.amazon.in",
            "Myntra": "https://www.myntra.com",
            "Zara": "https://www.zara.com/in/"
        }
    }

# -------- ROUTES --------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gender = request.form["gender"]
        photo = request.files["photo"]

        image_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        photo.save(image_path)

        skin_tone = detect_skin_tone(image_path)
        recommendation = get_style_recommendation(skin_tone, gender)

        return render_template(
            "index.html",
            skin_tone=skin_tone,
            recommendation=recommendation,
            gender=gender
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)