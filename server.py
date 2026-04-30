from flask import Flask, request, send_file
import os
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "PS2 to PKG Server is running!"

@app.route('/convert', methods=['POST'])
def convert():
    if 'iso' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['iso']
    
    # حفظ الملف مؤقتاً
    tmp = tempfile.mkdtemp()
    input_path = os.path.join(tmp, file.filename)
    file.save(input_path)
    
    # اسم الملف الناتج
    output_path = input_path.replace('.iso', '.pkg').replace('.ISO', '.pkg')
    
    try:
        # استخدام ps2classic للتشفير الحقيقي
        result = subprocess.run(
            ['ps2classic', '--encrypt', input_path, output_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            return f'Conversion failed: {result.stderr}', 500
        
        return send_file(output_path, as_attachment=True)
    
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
