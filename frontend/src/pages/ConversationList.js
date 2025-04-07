import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';

const ConversationList = () => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log("Fetching conversations from API...");
        const response = await axios.get('http://localhost:5000/api/conversations');
        console.log("API Response:", response.data);
        
        // Check if the conversations property exists
        if (response.data && response.data.conversations) {
          setConversations(response.data.conversations);
        } else {
          console.log("No conversations property in response");
          setConversations([]);
        }
      } catch (err) {
        console.error('Error fetching conversations:', err);
        setError('Failed to load conversations. Please make sure the API server is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  const handleConversationClick = (id) => {
    navigate(`/conversations/${id}`);
  };

  const formatTimestamp = (unixTimestamp) => {
    if (!unixTimestamp) return 'Unknown time';
    return new Date(unixTimestamp * 1000).toLocaleString();
  };

  const handleDeleteConversation = async (e, id) => {
    e.stopPropagation(); // Prevent navigation
    
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      try {
        await axios.delete(`http://localhost:5000/api/conversations/${id}`);
        // Update the conversations list
        setConversations(conversations.filter(conv => conv.conversation_id !== id));
      } catch (err) {
        console.error('Error deleting conversation:', err);
        setError('Failed to delete conversation. Please try again.');
      }
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="conversations-list">
      <h1 className="mb-4">Your Conversations</h1>
      
      {error && <ErrorAlert message={error} />}
      
      {conversations.length === 0 ? (
        <div className="alert alert-info">
          <h4>No conversations found.</h4>
          <p>There are a few possible reasons:</p>
          <ol>
            <li>You haven't created any conversations yet. Run agent1.py or agent2.py to create one.</li>
            <li>Your API key might not be properly set. Check ELEVENLABS_API_KEY1 or ELEVENLABS_API_KEY2 environment variables.</li>
            <li>The Flask server might not be connecting to the ElevenLabs API correctly.</li>
          </ol>
          <p>Check the console logs for more details.</p>
        </div>
      ) : (
        <div className="row">
          {conversations.map((conversation) => (
            <div className="col-md-6 mb-4" key={conversation.conversation_id}>
              <div 
                className="card conversation-card" 
                onClick={() => handleConversationClick(conversation.conversation_id)}
              >
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start">
                    <h5 className="card-title">
                      {conversation.agent_name || 'Conversation with AI'}
                    </h5>
                    <button 
                      className="btn btn-sm btn-outline-danger"
                      onClick={(e) => handleDeleteConversation(e, conversation.conversation_id)}
                    >
                      Delete
                    </button>
                  </div>
                  <h6 className="card-subtitle mb-2 text-muted">
                    ID: {conversation.conversation_id}
                  </h6>
                  <p className="card-text">
                    <small className="text-muted">
                      Status: {conversation.status || 'Unknown'}
                    </small>
                  </p>
                  <p className="card-text">
                    <small className="text-muted">
                      Started: {formatTimestamp(conversation.start_time_unix_secs)}
                    </small>
                  </p>
                  <p className="card-text">
                    <small className="text-muted">
                      Duration: {conversation.call_duration_secs || 0} seconds
                    </small>
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ConversationList; 