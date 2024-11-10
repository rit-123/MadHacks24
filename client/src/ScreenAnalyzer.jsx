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
        <button
            className="px-6 py-1.5 text-white bg-black border-2 border-white rounded-lg
                           transition-transform duration-300 hover:scale-105"
            style={{
                fontFamily: 'Arial Black, sans-serif',
                letterSpacing: '0.05em',
                textShadow: '0 0 10px rgba(255, 255, 255, 0.8)',
                boxShadow: `0 0 15px rgba(255, 255, 255, 0.5),
                             0 0 25px rgba(135, 206, 250, 0.8)`,
                fontSize: '18px',
                position: 'relative',
                background: 'black',
                border: '2px solid white',
                marginBottom: "70px"
            }}
            onClick={isCapturing ? stopCapture : startCapture}>
            {status === 'requesting' ? 'Requesting Permission...' :
                isCapturing ? 'STOP' :
                    'START'}
        </button>
    );
};

export default ScreenAnalyzer;