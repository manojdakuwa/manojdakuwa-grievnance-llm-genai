from backend.apps.services.ai_solution import SolutionService
from flask import Blueprint, request, jsonify
from backend.apps.models.grievance import Assignment, Grievance, GRO
from backend.apps.models.users import User
from backend.apps.utils.db import db
from backend.apps.services.image_processing import ImageProcessingService
from backend.apps.services.ai_services import ConversationalAIService
import os
from flask_cors import CORS
import joblib

grievance_bp = Blueprint('grievances', __name__)
CORS(grievance_bp)

solution_service = SolutionService()
# # Load the trained model and vectorizer
# clf = joblib.load('grievance_classifier.pkl')
# vectorizer = joblib.load('tfidf_vectorizer.pkl')

@grievance_bp.route('/', methods=['POST'])
def file_grievance():
    try:
        description = request.form['description']
        category = request.form['category']
        user_id = request.form['userId']
        parent_id = request.form.get('parentId') 

        # # Automatic categorisation
        # description_vec = vectorizer.transform([description])
        # predicted_category = clf.predict(description_vec)[0]
        # # Map to department (for simplicity, let's assume each category maps to a specific department)
        # department_map = {
        #     'Category1': 'Department1',
        #     'Category2': 'Department2',
        #     'Category3': 'Department3'
        # }
        # department = department_map.get(predicted_category, 'General')
        # print("description: ", description)
        # print("category: ", category)
        # print("user_id: ", user_id)
        # Initialize conversational AI service
        ai_service = ConversationalAIService()
        ai_response = ai_service.generate_response(description)
        
        new_grievance = Grievance(description=description + f" (AI Response: {ai_response})", category=category, user_id=user_id, parent_id=parent_id)
        
        # Process image if present
        if 'image' in request.files:
            image = request.files['image']
            image_path = os.path.join('uploads', image.filename)
            image.save(image_path)
            
            image_service = ImageProcessingService()
            image_description = image_service.describe_image(image_path)
            ocr_text = image_service.extract_text_from_image(image_path)
            new_grievance.description += f" (Image Analysis: {image_description}) (OCR: {ocr_text})"
        
        db.session.add(new_grievance)
        db.session.commit()
        
        return jsonify({"message": "Grievance filed successfully", "ai_response": ai_response, "status": 201})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e), "status":500})
@grievance_bp.route('/', methods=['GET'])
def get_grievances():
    try:
        grievances = Grievance.query.all()
        print("grievances: ", grievances)
        grievances_list = [
            {
                "id": g.id,
                "description": g.description,
                "category": g.category,
                "status": g.status,
                "user_id": g.user_id,
                "parent_id": g.parent_id,
                "assignments": [{"gro_id": a.gro_id, "gro_name": GRO.query.get(a.gro_id).name} for a in g.assignments]
            } for g in grievances
        ]
        return jsonify(grievances_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
@grievance_bp.route('/assign', methods=['POST'])
def assign_gro():
    try:
        grievance_id = request.form['grievanceId']
        gro_id = request.form['groId']
        assignment = Assignment(grievance_id=grievance_id, gro_id=gro_id)
        db.session.add(assignment)
        db.session.commit()
        return jsonify({"message": "GRO assigned successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    

@grievance_bp.route('/solution', methods=['POST'])
def get_solution():
    try:
        description = request.form['description']
        category = request.form['category']
        language = request.form.get('language', 'en')
        solution = solution_service.get_solution_suggestion(description, category, language)
        return jsonify({"solution": solution}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500