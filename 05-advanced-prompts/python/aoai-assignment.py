from flask import Flask, Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import html

# Initialize the Flask app
app = Flask(__name__)

# Set up rate limiting (100 requests per hour per IP)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100/hour"])

# Create a blueprint for modular structure
api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
@limiter.limit("10/minute")  # Example route-specific limit
def hello():
    try:
        name = request.args.get('name', 'World')
        safe_name = html.escape(name.strip())[:50]  # Sanitize & limit length
        return jsonify({'message': f'Hello, {safe_name}!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Custom 404 JSON response
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

# Register the blueprint
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)