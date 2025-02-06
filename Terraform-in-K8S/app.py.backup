from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-terraform', methods=['POST'])
def run_terraform():
    payload = request.json
    command = payload.get('command')
    if not command:
        return jsonify({'error': 'Command not provided'}), 400
    
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return jsonify({'output': result.stdout, 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
