import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from conversation_manager import ConversationManager

app = Flask(__name__, static_folder='frontend/build')
CORS(app)  # Enable CORS for all routes

# Get API key from environment
api_key = os.getenv("ELEVENLABS_API_KEY1") or os.getenv("ELEVENLABS_API_KEY2")
if not api_key:
    print("Warning: No API key found in environment variables.")
    print("Please set ELEVENLABS_API_KEY1 or ELEVENLABS_API_KEY2.")

# Initialize the conversation manager
manager = ConversationManager(api_key=api_key)

@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """API endpoint to list all conversations"""
    try:
        conversations = manager.list_conversations()
        
        # Convert Pydantic model to dict
        if hasattr(conversations, 'model_dump'):
            conversations_dict = conversations.model_dump()
        else:
            conversations_dict = conversations.dict()
            
        return jsonify(conversations_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """API endpoint to get details of a specific conversation"""
    try:
        details = manager.get_conversation_details(conversation_id)
        
        # Convert Pydantic model to dict
        if hasattr(details, 'model_dump'):
            details_dict = details.model_dump()
        else:
            details_dict = details.dict()
            
        return jsonify(details_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """API endpoint to delete a conversation"""
    try:
        response = manager.delete_conversation(conversation_id)
        return jsonify({"success": True, "message": f"Conversation {conversation_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations/<conversation_id>/save', methods=['POST'])
def save_conversation(conversation_id):
    """API endpoint to save a conversation transcript"""
    try:
        filename = request.json.get('filename') if request.json else None
        success = manager.save_conversation_transcript(conversation_id, filename)
        
        if success:
            return jsonify({"success": True, "message": f"Conversation saved successfully", "filename": filename})
        else:
            return jsonify({"error": "Failed to save conversation"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve React frontend in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000) 