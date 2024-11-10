import React, { useState, useEffect } from 'react';

const ScreenAnalyzer = () => {
  const [stream, setStream] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [lastProcessed, setLastProcessed] = useState(null);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [status, setStatus] = useState('idle'); // 'idle', 'requesting', 'active', 'error'

  const processAndSendFrame = async (canvas) => {
    try {
      setIsProcessing(true);
      const base64Data = canvas.toDataURL('image/jpeg', 0.8);
      
      const payload = {
        timestamp: new Date().toISOString(),
        imageData: base64Data,
        screenWidth: canvas.width,
        screenHeight: canvas.height
      };
      console.log(base64Data);
      const response = await fetch('http://localhost:5000/screenshot', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Failed to process screen data');
      }

      const result = await response.json();
      setLastProcessed({
        timestamp: new Date().toLocaleTimeString(),
        recommendation: result.recommendation
      });
      setStatus('active');
      
    } catch (err) {
      console.error('Error processing screen:', err);
      setError('Failed to process screen data. Please try again.');
      setStatus('error');
    } finally {
      setIsProcessing(false);
    }
  };

  const startCapture = async () => {
    try {
      setError(null);
      setStatus('requesting');
      
      const mediaStream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          cursor: 'never'
        },
        audio: false
      });
      
      setStream(mediaStream);
      setIsCapturing(true);
      setStatus('active');
      
      mediaStream.getVideoTracks()[0].addEventListener('ended', () => {
        stopCapture();
      });
    } catch (err) {
      console.error('Error accessing screen:', err);
      setError('Permission denied or screen share cancelled. Please try again.');
      setStatus('error');
      setIsCapturing(false);
    }
  };

  const stopCapture = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsCapturing(false);
    setLastProcessed(null);
    setStatus('idle');
  };

  useEffect(() => {
    let intervalId;

    if (isCapturing && stream) {
      intervalId = setInterval(() => {
        const video = document.createElement('video');
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
          const canvas = document.createElement('canvas');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          
          const ctx = canvas.getContext('2d');
          ctx.drawImage(video, 0, 0);
          
          processAndSendFrame(canvas);
          
          video.remove();
          canvas.remove();
        };
        
        video.play();
      }, 15000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isCapturing, stream]);

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex items-center justify-center">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-6">
          Screen Activity Analyzer
        </h1>

        <div className="space-y-6">
          {/* Main Action Button */}
          <div className="flex justify-center">
            <button
              onClick={isCapturing ? stopCapture : startCapture}
              className={`
                w-full max-w-sm py-3 px-6 rounded-lg font-semibold text-white
                transform transition-all duration-200 
                ${status === 'requesting' ? 'bg-yellow-500 hover:bg-yellow-600' :
                  isCapturing ? 'bg-red-500 hover:bg-red-600' : 
                  'bg-blue-500 hover:bg-blue-600'} 
                ${status === 'requesting' ? 'animate-pulse' : ''}
              `}
            >
              {status === 'requesting' ? 'Requesting Permission...' :
               isCapturing ? 'Stop Screen Analysis' : 
               'Start Screen Analysis'}
            </button>
          </div>

          {/* Status Messages */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {isProcessing && (
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <p className="text-blue-700">Processing your screen...</p>
            </div>
          )}

          {/* Information Panel */}
          {isCapturing && !error && (
            <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
              <p className="text-green-700 font-medium">Screen analysis is active</p>
              <p className="text-green-600 text-sm mt-1">
                Analyzing your screen every 30 seconds
              </p>
            </div>
          )}

          {/* Results Panel */}
          {lastProcessed && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="font-medium text-gray-700 mb-2">
                Latest Analysis Results
              </h3>
              <p className="text-sm text-gray-600">
                Time: {lastProcessed.timestamp}
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Recommendation: {lastProcessed.recommendation}
              </p>
            </div>
          )}

          {/* Instructions Panel */}
          {!isCapturing && !error && (
            <div className="text-gray-600 text-sm space-y-2">
              <p>Click the button above to:</p>
              <ol className="list-decimal list-inside space-y-1 ml-2">
                <li>Grant permission to analyze your screen</li>
                <li>Select which window or screen to analyze</li>
                <li>Get personalized music recommendations</li>
              </ol>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-xs text-gray-500">
          Your privacy is important. Screen data is processed locally and only 
          analyzed to provide music recommendations.
        </div>
      </div>
    </div>
  );
};

export default ScreenAnalyzer;