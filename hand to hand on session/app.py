from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import time
from werkzeug.utils import secure_filename

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


if __name__ == "__main__":
    app.run(debug=True)
