from flask import Blueprint, request, jsonify
from grievance_system.services.gemini_service import analyze_complaint

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze', methods=['POST'])
def analyze():
    data        = request.get_json()
    title       = data.get('title', '')
    description = data.get('description', '')
    if not title and not description:
        return jsonify({'error': 'No input provided'}), 400
    result = analyze_complaint(title, description)
    return jsonify(result)