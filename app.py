from flask import Flask, render_template, request, jsonify
import qrcode
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

LOGO_PATH = os.path.join("static", "logo.png")  # put your logo here

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    url = data["url"]
    color = data["color"]
    use_logo = data["logo"]

    qr = qrcode.QRCode(
        version=3,
        box_size=8,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=color, back_color="white").convert("RGB")

    if use_logo and os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        qr_w, qr_h = qr_img.size
        logo_size = qr_w // 4
        logo = logo.resize((logo_size, logo_size))
        pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return jsonify({"image": img_str})

if __name__ == "__main__":
    app.run(debug=True)
