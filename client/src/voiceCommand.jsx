import React, { useState, useEffect, useRef } from 'react';

const VoiceCommandListener = ({ targetWord, onWordDetected }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  const [hasPermission, setHasPermission] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    // Check if browser supports speech recognition
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition is not supported in this browser');
      return;
    }

    // Initialize speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();

    recognitionRef.current.continuous = true;
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = 'en-US';

    recognitionRef.current.onstart = () => {
      setIsListening(true);
      setError(null);
    };

    recognitionRef.current.onerror = (event) => {
      if (event.error === 'not-allowed') {
        setError('Microphone permission denied. Please allow microphone access.');
        setHasPermission(false);
      } else {
        setError(`Speech recognition error: ${event.error}`);
      }
      setIsListening(false);
    };

    recognitionRef.current.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current.onresult = (event) => {
      const currentTranscript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join(' ')
        .toLowerCase();
      
      setTranscript(currentTranscript);

      if (currentTranscript.includes(targetWord.toLowerCase())) {
        onWordDetected();
      }
    };

    // Check for microphone permission
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(() => {
        setHasPermission(true);
        setError(null);
      })
      .catch(() => {
        setHasPermission(false);
        setError('Microphone permission denied. Please allow microphone access.');
      });

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [targetWord, onWordDetected]);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      try {
        recognitionRef.current?.start();
      } catch (err) {
        setError('Error starting speech recognition. Try stopping and starting again.');
      }
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <div className="mb-4 flex items-center justify-between">
        <p className="font-medium">
          Status: {isListening ? 'Listening...' : 'Not listening'}
        </p>
        <button
          onClick={toggleListening}
          disabled={!hasPermission}
          className={`px-4 py-2 rounded ${
            isListening 
              ? 'bg-red-500 hover:bg-red-600 text-white' 
              : 'bg-green-500 hover:bg-green-600 text-white'
          } ${!hasPermission ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isListening ? 'Stop' : 'Start'} Listening
        </button>
      </div>
      {error && (
        <p className="text-red-500 mt-2 mb-4">
          {error}
        </p>
      )}
      <div className="mt-4">
        <p className="text-sm text-gray-600">Transcript:</p>
        <p className="mt-1 p-2 bg-white border rounded">
          {transcript || 'No speech detected yet...'}
        </p>
      </div>
    </div>
  );
};

export default VoiceCommandListener;