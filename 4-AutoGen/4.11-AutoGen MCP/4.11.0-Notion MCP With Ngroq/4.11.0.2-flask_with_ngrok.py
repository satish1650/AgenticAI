import os
from flask import Flask, jsonify
from dotenv import load_dotenv 
from pyngrok import ngrok
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

ngroq_aut_token = os.getenv('NGROK_AUTH_TOKEN')
if not ngroq_aut_token:
    raise ValueError("NGROK_AUTH_TOKEN is not set in the environment variables.")   

# Initialize Flask app and CORS
app= Flask(__name__)
CORS(app)

# Define a simple route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Windows via Terminal!"})   

# Set up ngrok tunnel
if __name__ == '__main__':
    port=7001
    os.environ['FLASK_ENV'] = 'development'

    ngrok.set_auth_token(ngroq_aut_token)
    public_url= ngrok.connect(port)
    print(f"Public URL: {public_url}/api/hello \n \n")

    app.run(port=port)