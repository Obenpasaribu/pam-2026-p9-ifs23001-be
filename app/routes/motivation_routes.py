from flask import Blueprint, request, jsonify
from app.services.motivation_service import (
    create_fashion_advice,
    get_all_fashion_advice
)

motivation_bp = Blueprint("motivation", __name__)

@motivation_bp.route("/", methods=["GET"])
def index():
    return "API Fashion Stylist telah berjalan!"
    

@motivation_bp.route("/fashion/generate", methods=["POST"])
def generate():
    data = request.get_json()
    skin_tone = data.get("skin_tone")
    total = data.get("total")

    if not skin_tone:
        return jsonify({"error": "Skin tone is required"}), 400
    
    if not total:
        return jsonify({"error": "Total is required"}), 400
    
    if total <= 0:
        return jsonify({"error": "Total harus besar dari 0"}), 400
    
    if total > 10:
        return jsonify({"error": "Total maksimal harus 10"}), 400

    try:
        result = create_fashion_advice(skin_tone, total)

        return jsonify({
            "skin_tone": skin_tone,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motivation_bp.route("/fashion", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    data = get_all_fashion_advice(page=page, per_page=per_page)

    return jsonify(data)
