import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import base64
from PIL import Image
import io
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/validate": {"origins": os.getenv('CORS_ORIGIN', 'http://localhost')}})
debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']

@app.route('/validate', methods=['POST'])
def validateFaces():
    nombre_archivo = ""
    nombre_url = ""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()

        base64_image = data['imageBase64'].split(',')[1]
        image_url = data['imageUrl']

        img_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(img_bytes))
        nombre_archivo = f"{uuid.uuid4()}.jpg"
        img.save(nombre_archivo)

        result = DeepFace.verify(image_url, nombre_archivo, model_name='Facenet', enforce_detection=False)

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
    app.run(debug=debug, host='0.0.0.0', port=5000)
