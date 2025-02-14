from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

import os
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "files" not in request.files:
            return "No file part"

        files = request.files.getlist("files")  # Get multiple files

        for file in files:
            if file.filename:  # Check if file is selected
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

        return redirect(url_for("manage_uploads"))

    return render_template("index.html")


# Manage Uploads (View, Delete, Print)
@app.route("/manage", methods=["GET", "POST"])
def manage_uploads():
    files = os.listdir(app.config["UPLOAD_FOLDER"])  # List all files

    if request.method == "POST":
        action = request.form.get("action")
        filename = request.form.get("filename")

        if action == "delete":
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        return redirect(url_for("manage_uploads"))

    return render_template("manage.html", files=files)


# Serve files for viewing/printing
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)