import React, { useState } from 'react';
import Question from './Question';

const QuestionGenerator = () => {
  const [questions, setQuestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const generateQuestions = async () => {
    setIsLoading(true);
    setError('');
    setQuestions([]);
    
    try {
      // Simulate API call - replace with your actual implementation
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // TODO: Replace this with your actual question generation logic
      const generatedQuestions = [
        "What is the main purpose of RAG (Retrieval-Augmented Generation)?",
        "How does the document retrieval process work in this application?",
        "What are the key components of the like-a-RAG-test system?",
        "How does the application handle context windows during question answering?",
        "What embedding model is used for document vectorization?"
      ];
      
      setQuestions(generatedQuestions);
    } catch (err) {
      console.error('Error generating questions:', err);
      setError('Error generating questions. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h1 className="text-center mb-2">Question Generator</h1>
        <p className="text-center text-muted mb-4">Generate automatic questions from your data with one click</p>
        
        <div className="d-flex justify-content-center mb-4">
          <button 
            className="btn btn-primary btn-lg px-4" 
            onClick={generateQuestions}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Generating...
              </>
            ) : (
              'Generate Questions'
            )}
          </button>
        </div>
        
        <div className="mt-4 pt-3 border-top">
          <h2>Generated Questions</h2>
          
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          {!isLoading && questions.length === 0 && !error && (
            <p className="text-muted">No questions generated yet. Click the button above to start.</p>
          )}
          
          <div className="mt-3">
            {questions.map((question, index) => (
              <Question key={index} text={question} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionGenerator;