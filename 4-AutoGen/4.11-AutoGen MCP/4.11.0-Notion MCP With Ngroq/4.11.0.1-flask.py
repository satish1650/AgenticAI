import os
from flask import Flask, jsonify


app= Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Windows via Terminal!"})   

if __name__ == '__main__':
    port= 7001
    os.environ['FLASK_ENV'] = 'development'

    app.run(port=port)