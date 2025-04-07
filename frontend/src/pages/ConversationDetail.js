import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';

const ConversationDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [conversation, setConversation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    const fetchConversationDetails = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`http://localhost:5000/api/conversations/${id}`);
        setConversation(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching conversation details:', err);
        setError('Failed to load conversation details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchConversationDetails();
  }, [id]);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      try {
        await axios.delete(`http://localhost:5000/api/conversations/${id}`);
        navigate('/');
      } catch (err) {
        console.error('Error deleting conversation:', err);
        setError('Failed to delete conversation. Please try again.');
      }
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setSaveSuccess(false);
      
      const filename = `conversation_${id}.txt`;
      await axios.post(`http://localhost:5000/api/conversations/${id}/save`, { filename });
      
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000); // Hide success message after 3 seconds
    } catch (err) {
      console.error('Error saving conversation:', err);
      setError('Failed to save conversation. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  if (!conversation) {
    return (
      <div className="alert alert-warning">
        Conversation not found or has been deleted.
      </div>
    );
  }

  // Format and display the conversation transcript
  const formatTimestamp = (unixTimestamp) => {
    if (!unixTimestamp) return '';
    return new Date(unixTimestamp * 1000).toLocaleString();
  };

  return (
    <div className="conversation-detail">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Conversation Details</h1>
        <div>
          <button 
            className="btn btn-primary me-2" 
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Transcript'}
          </button>
          <button 
            className="btn btn-danger" 
            onClick={handleDelete}
          >
            Delete
          </button>
        </div>
      </div>

      {error && <ErrorAlert message={error} />}
      
      {saveSuccess && (
        <div className="alert alert-success">
          Conversation transcript saved successfully!
        </div>
      )}

      <div className="card mb-4">
        <div className="card-header">
          <h5 className="mb-0">Conversation Information</h5>
        </div>
        <div className="card-body">
          <p><strong>ID:</strong> {conversation.conversation_id}</p>
          <p><strong>Agent ID:</strong> {conversation.agent_id}</p>
          <p>
            <strong>Start Time:</strong> {formatTimestamp(conversation.metadata?.start_time_unix_secs)}
          </p>
          <p>
            <strong>Duration:</strong> {conversation.metadata?.call_duration_secs || 0} seconds
          </p>
          <p><strong>Status:</strong> {conversation.status || 'Unknown'}</p>
        </div>
      </div>

      <h3 className="mb-3">Transcript</h3>
      
      {!conversation.transcript || conversation.transcript.length === 0 ? (
        <div className="alert alert-info">
          No transcript available for this conversation.
        </div>
      ) : (
        <div className="card">
          <div className="card-body conversation-messages">
            {conversation.transcript.map((message, index) => (
              <div 
                key={index}
                className={`message-bubble ${message.role === 'user' ? 'user-message' : 'agent-message'}`}
              >
                <div className="message-header mb-1">
                  <small>
                    {message.role === 'user' ? 'You' : 'Agent'} 
                    {message.time_in_call_secs && ` (${message.time_in_call_secs}s)`}
                  </small>
                </div>
                <div>{message.message}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ConversationDetail; 