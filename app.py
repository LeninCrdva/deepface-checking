import os
from flask import Flask, request, jsonify
from deepface import DeepFace
import base64
from PIL import Image
import io
import uuid

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validateFaces():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()

        base64_image = data['imageBase64'].split(',')[1]
        image_url = data['imageUrl']

        response = request.get(image_url)

        if response.status_code != 200:
            return jsonify({'error': 'No se pudo descargar la imagen desde la URL proporcionada'}), 400

        img2 = Image.open(io.BytesIO(response.content))
        nombre_url = f"{uuid.uuid4()}.jpg"
        img2.convert("RGB").save(nombre_url)

        img_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(img_bytes))
        nombre_archivo = f"{uuid.uuid4()}.jpg"
        img.save(nombre_archivo)

        result = DeepFace.verify(nombre_archivo, nombre_url, model_name='Facenet')

        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)
        if os.path.exists(nombre_url):
            os.remove(nombre_url)
    
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Método no permitido',
        'message': 'El método HTTP no está permitido para esta ruta'
    }), 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
