import os
import glob

from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from src.csv.creator import create_csv_file
from settings import SERVER_HOST, SERVER_PORT, LOCAL, UPLOAD_DIR


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']

        if request.form['password'] == "password123" and username == "root":

            return render_template("file_upload_form.html")

    return render_template("login.html")


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = []
    csv_option = request.form["csvOption"]

    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file_name = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if ".pdf" in file_name:
                file.save(file_path)
                uploaded_files.append(file_path)

        result_file = create_csv_file(file_paths=uploaded_files, option=csv_option)

        return send_file(result_file, as_attachment=True)


if __name__ == '__main__':

    for u_file in glob.glob(os.path.join(UPLOAD_DIR, "*.*")):
        os.remove(u_file)

    if LOCAL:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    else:
        app.run(debug=False, host=SERVER_HOST, port=SERVER_PORT)
