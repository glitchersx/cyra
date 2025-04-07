#!/usr/bin/env python3
import os
from conversation_manager import ConversationManager

def print_separator():
    """Print a separator line."""
    print("\n" + "-" * 50 + "\n")

def main():
    """Demonstrate conversation management features."""
    # Get API key from environment
    api_key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY2")
    
    if not api_key:
        print("Error: No API key found in environment variables.")
        print("Please set ELEVENLABS_API_KEY1 or ELEVENLABS_API_KEY2.")
        return
    
    # Create manager instance
    manager = ConversationManager(api_key=api_key)
    
    # Example 1: List all conversations
    print("LISTING ALL CONVERSATIONS")
    print_separator()
    
    conversations = manager.list_conversations()
    
    # Check if conversations object exists and has conversations attribute
    if not conversations or not hasattr(conversations, 'conversations') or not conversations.conversations:
        print("No conversations found. Run agent1.py or agent2.py to create a conversation first.")
        return
    
    # Display basic info for each conversation
    for idx, convo in enumerate(conversations.conversations):
        print(f"Conversation {idx+1}:")
        
        # Access attributes directly instead of using .get()
        convo_id = convo.conversation_id if hasattr(convo, 'conversation_id') else "Unknown"
        agent_name = convo.agent_name if hasattr(convo, 'agent_name') else "Unknown"
        status = convo.status if hasattr(convo, 'status') else "Unknown"
        duration = convo.call_duration_secs if hasattr(convo, 'call_duration_secs') else 0
        
        print(f"  ID: {convo_id}")
        print(f"  Agent: {agent_name}")
        print(f"  Status: {status}")
        print(f"  Duration: {duration} seconds")
        print()
    
    # Check again if conversations list is empty (for safety)
    if not conversations.conversations:
        return
        
    # Select a conversation for further operations
    selected_convo = conversations.conversations[0]
    convo_id = selected_convo.conversation_id if hasattr(selected_convo, 'conversation_id') else None
    
    if not convo_id:
        print("Could not find a valid conversation ID.")
        return
    
    # Example 2: Get conversation details
    print_separator()
    print(f"GETTING DETAILS FOR CONVERSATION: {convo_id}")
    print_separator()
    
    details = manager.get_conversation_details(convo_id)
    
    if details and hasattr(details, 'transcript') and details.transcript:
        print(f"Conversation with {len(details.transcript)} messages:")
        for idx, msg in enumerate(details.transcript):
            # Access attributes directly
            role = msg.role if hasattr(msg, 'role') else "unknown"
            message = msg.message if hasattr(msg, 'message') else "[message missing]"
            print(f"{idx+1}. {role.capitalize()}: {message}")
    else:
        print("No transcript available for this conversation.")
    
    # Example 3: Save conversation to file
    print_separator()
    print(f"SAVING CONVERSATION {convo_id} TO FILE")
    print_separator()
    
    filename = f"saved_conversation_{convo_id}.txt"
    if manager.save_conversation_transcript(convo_id, filename):
        print(f"Conversation saved to {filename}")
    
    # Example 4: Delete conversation (uncomment to enable)
    """
    print_separator()
    print(f"DELETING CONVERSATION {convo_id}")
    print_separator()
    
    if manager.delete_conversation(convo_id):
        print(f"Conversation {convo_id} deleted successfully")
    else:
        print(f"Failed to delete conversation {convo_id}")
    """
    
    print_separator()
    print("DEMO COMPLETED")
    print("For more operations, use the conversation_manager.py script directly.")
    print("Run: python conversation_manager.py --help")

if __name__ == "__main__":
    main() 