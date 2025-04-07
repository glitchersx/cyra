import React from 'react';

const ErrorAlert = ({ message }) => {
  return (
    <div className="alert alert-danger" role="alert">
      {message || 'An error occurred. Please try again.'}
    </div>
  );
};

export default ErrorAlert; 