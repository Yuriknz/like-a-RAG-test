import React from 'react';

const Question = ({ text }) => {
  return (
    <div className="card mb-3 border-start border-primary border-4">
      <div className="card-body py-3">
        {text}
      </div>
    </div>
  );
};

export default Question;