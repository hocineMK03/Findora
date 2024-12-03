

from flask import Blueprint, request, jsonify

from src.services.SearchServices import SearchServices
search = Blueprint('search', __name__)




@search.route('/search', methods=['POST'])
def retrieveDocs():
    
    data=request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    try:
        request_data=data['request']
        
        searchServices=SearchServices()
        result=searchServices.handleRetrieveDocs(request_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
    return jsonify(result)
    
    
@search.route('/searchspecific', methods=['POST'])
def retrieveSpecificDocs():
    data=request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    try:
        request_data=data['document']
        searchServices=SearchServices()
        result=searchServices.handleSearchSpecificDoc(request_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
    return jsonify(result)