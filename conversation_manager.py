import os
import argparse
import json
from elevenlabs.client import ElevenLabs
import time

class ConversationManager:
    def __init__(self, api_key=None):
        """Initialize the conversation manager with the provided API key.
        
        Args:
            api_key (str, optional): ElevenLabs API key. If not provided, will try to load from environment.
        """
        # Try to get API key from environment if not provided
        if api_key is None:
            api_key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY2")
            if not api_key:
                raise ValueError("API key not provided and not found in environment variables")
        
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=api_key)
    
    def list_conversations(self):
        """List all available conversations.
        
        Returns:
            object: Response containing conversation list
        """
        try:
            response = self.client.conversational_ai.get_conversations()
            return response
        except Exception as e:
            print(f"Error listing conversations: {e}")
            return None
    
    def get_conversation_details(self, conversation_id):
        """Get details of a specific conversation.
        
        Args:
            conversation_id (str): ID of the conversation to retrieve
            
        Returns:
            object: Response containing conversation details
        """
        try:
            response = self.client.conversational_ai.get_conversation(conversation_id)
            return response
        except Exception as e:
            print(f"Error retrieving conversation {conversation_id}: {e}")
            return None
    
    def delete_conversation(self, conversation_id):
        """Delete a specific conversation.
        
        Args:
            conversation_id (str): ID of the conversation to delete
            
        Returns:
            object: Response from the delete operation
        """
        try:
            response = self.client.conversational_ai.delete_conversation(conversation_id)
            return response
        except Exception as e:
            print(f"Error deleting conversation {conversation_id}: {e}")
            return None
    
    def save_conversation_transcript(self, conversation_id, filename=None):
        """Save a conversation transcript to a file.
        
        Args:
            conversation_id (str): ID of the conversation to save
            filename (str, optional): Name of the file to save to. If not provided,
                                     a default name based on the conversation ID will be used.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get conversation details
            conv_data = self.get_conversation_details(conversation_id)
            
            if not conv_data:
                return False
            
            # Access transcript attribute safely
            transcript = None
            if hasattr(conv_data, 'transcript'):
                transcript = conv_data.transcript
            
            if transcript is None:
                print("Error: Transcript not found in API response.")
                return False
            elif not transcript:
                print("Warning: Transcript is empty.")
                return False
            
            # Format conversation history
            history = []
            for entry in transcript:
                # Access attributes directly instead of using .get()
                role = "User" if hasattr(entry, 'role') and entry.role == 'user' else "Agent"
                message = entry.message if hasattr(entry, 'message') else '[message missing]'
                # Attempt to get timestamp - adjust 'timestamp' attribute name if needed based on API response structure
                timestamp_str = ""
                if hasattr(entry, 'timestamp'):
                    # Format the timestamp nicely if it exists (e.g., ISO format, local time)
                    # This is a placeholder - actual formatting depends on the timestamp data type
                    try:
                        timestamp_str = f"[{entry.timestamp}] " 
                    except Exception:
                        timestamp_str = "[timestamp error] " # Handle potential formatting errors
                
                history.append(f"{timestamp_str}{role}: {message}")
            
            # Determine filename
            conversation_dir = "conversations"
            os.makedirs(conversation_dir, exist_ok=True) # Ensure directory exists
            
            if not filename:
                # Use a timestamp for more robust naming
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                base_filename = f"conversation_{conversation_id}_{timestamp}.txt"
            else:
                # Ensure provided filename doesn't have path separators and ends with .txt
                base_filename = os.path.basename(filename)
                if not base_filename.endswith('.txt'):
                    base_filename += '.txt'
            
            full_path = os.path.join(conversation_dir, base_filename)
            
            # Write to file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(history))
            
            print(f"Conversation successfully saved to {full_path}")
            return True
            
        except Exception as e:
            print(f"Failed to save conversation. Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Command line interface for the conversation manager."""
    parser = argparse.ArgumentParser(description="Manage ElevenLabs AI conversations")
    
    # Add API key argument
    parser.add_argument("--api-key", help="ElevenLabs API key")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all conversations")
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Get details of a conversation")
    get_parser.add_argument("id", help="Conversation ID")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a conversation")
    delete_parser.add_argument("id", help="Conversation ID")
    
    # Save command
    save_parser = subparsers.add_parser("save", help="Save a conversation transcript to a file")
    save_parser.add_argument("id", help="Conversation ID")
    save_parser.add_argument("--file", help="Output filename")
    
    args = parser.parse_args()
    
    # Create manager instance
    try:
        manager = ConversationManager(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Execute command
    if args.command == "list":
        conversations = manager.list_conversations()
        if conversations:
            # For JSON serialization, use model_dump() if available (pydantic v2)
            # or dict() if not (pydantic v1)
            if hasattr(conversations, 'model_dump'):
                conversations_dict = conversations.model_dump()
            else:
                conversations_dict = conversations.dict()
            
            print(json.dumps(conversations_dict, indent=2))
            
            # Check for conversations attribute
            if hasattr(conversations, 'conversations') and conversations.conversations:
                print(f"\nFound {len(conversations.conversations)} conversation(s)")
            else:
                print("\nNo conversations found")
    
    elif args.command == "get":
        details = manager.get_conversation_details(args.id)
        if details:
            # For JSON serialization, use model_dump() if available (pydantic v2)
            # or dict() if not (pydantic v1)
            if hasattr(details, 'model_dump'):
                details_dict = details.model_dump()
            else:
                details_dict = details.dict()
                
            print(json.dumps(details_dict, indent=2))
    
    elif args.command == "delete":
        response = manager.delete_conversation(args.id)
        if response is not None:
            print(f"Conversation {args.id} deleted successfully")
        else:
            print(f"Failed to delete conversation {args.id}")
    
    elif args.command == "save":
        success = manager.save_conversation_transcript(args.id, args.file)
        if not success:
            print(f"Failed to save conversation {args.id}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 