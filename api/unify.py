import os
import csv
import json
import io
from flask import Flask, render_template, request, send_file
import sys
from datetime import datetime

# Ensure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.converter import convert_from_format1, convert_from_format2

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/unify", methods=["POST"])
def unify():
    file1 = request.files.get("file1")
    file2 = request.files.get("file2")

    if not file1 or not file2:
        return "Both JSON files must be uploaded.", 400

    try:
        json1 = json.load(file1)
        json2 = json.load(file2)

        unified_data = [
            convert_from_format1(json1) if "deviceID" in json1 else convert_from_format2(json1),
            convert_from_format1(json2) if "deviceID" in json2 else convert_from_format2(json2)
        ]
    except Exception as e:
        return f"Error: {str(e)}", 500

    return render_template("index.html", result=unified_data)


@app.route("/export_csv", methods=["POST"])
def export_csv():
    data = request.form.get("data")
    if not data:
        return "No data provided", 400

    unified_data = json.loads(data)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=unified_data[0].keys())
    writer.writeheader()
    writer.writerows(unified_data)

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                     as_attachment=True, download_name="unified_output.csv")


if __name__ == "__main__":
    app.run(debug=True)
