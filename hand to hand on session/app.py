from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, jsonify
import os
import time
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# ---------- CONFIG ----------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

online_users = set()


# ---------- TRACK USERS ----------
@app.before_request
def track_users():
    session.permanent = True
    online_users.add(request.remote_addr)


# ---------- DASHBOARD ----------
@app.route("/", methods=["GET", "POST"])
def dashboard():

    if request.method == "POST":
        reg_no = request.form["reg_no"]
        file = request.files["file"]

        if file and file.filename:
            safe_name = secure_filename(file.filename)
            filename = f"{reg_no}_{int(time.time())}_{safe_name}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return redirect(url_for("dashboard"))

    uploaded_files = []

    for file in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, file)

        if os.path.isfile(path):
            created_time = time.ctime(os.path.getctime(path))

            parts = file.split("_", 2)
            reg_no = parts[0]
            original_name = parts[2] if len(parts) == 3 else file

            uploaded_files.append({
                "reg_no": reg_no,
                "filename": original_name,
                "full_name": file,
                "time": created_time
            })

    uploaded_files.sort(
        key=lambda x: os.path.getctime(
            os.path.join(UPLOAD_FOLDER, x["full_name"])
        ),
        reverse=True
    )

    return render_template(
        "dashboard.html",
        users=len(online_users),
        total_files=len(uploaded_files),
        uploaded_files=uploaded_files
    )


# ---------- DOWNLOAD ----------
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ---------- VIEW ALL ----------
@app.route("/files")
def files():
    return render_template("files.html", files=os.listdir(UPLOAD_FOLDER))


# ---------- OCR: EXTRACT TEXT FROM IMAGE ----------
@app.route("/ocr", methods=["GET", "POST"])
def ocr_page():
    extracted_text = None
    filename = None
    
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            
            if image_file and image_file.filename:
                try:
                    # Open image and extract text using Tesseract
                    img = Image.open(image_file.stream)
                    extracted_text = pytesseract.image_to_string(img)
                    filename = secure_filename(image_file.filename)
                except Exception as e:
                    extracted_text = f"Error: {str(e)}"
        
        return render_template("ocr.html", extracted_text=extracted_text, filename=filename)
    
    return render_template("ocr.html", extracted_text=None, filename=None)


# ---------- API: OCR FROM UPLOADED FILE ----------
@app.route("/api/ocr", methods=["POST"])
def api_ocr():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    
    try:
        img = Image.open(file.stream)
        text = pytesseract.image_to_string(img)
        return jsonify({"success": True, "text": text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
