from logging import debug
from flask import Flask, request
from werkzeug.utils import secure_filename
from processing import read_excel

app = Flask(__name__, static_url_path="/static")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_path = secure_filename(file.filename)
    file.save("./static/" + file_path)

    read_excel(file_path)

    return "success"


if __name__ == "__main__":
    app.run(host="localhost", port="8080", debug=True)
