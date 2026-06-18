from io import BytesIO
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf_generator import build_pdf_from_data

app = Flask(__name__)
CORS(app)

@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Calypso PDF Backend funcionando"
    })

@app.post("/generar-pdf")
def generar_pdf():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"ok": False, "error": "No llegaron datos"}), 400

    pdf_buffer = BytesIO()
    build_pdf_from_data(pdf_buffer, data)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="cotizacion_calypso.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
