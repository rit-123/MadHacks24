import React, { useState, useEffect } from 'react';

const ScreenAnalyzer = ({ setSpinning }) => {
    // ADDED: New state variables for camera stream and status
    const [screenStream, setScreenStream] = useState(null);
    const [cameraStream, setCameraStream] = useState(null);
    const [isCapturing, setIsCapturing] = useState(false);
    const [lastProcessed, setLastProcessed] = useState(null);
    const [error, setError] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [status, setStatus] = useState('idle'); // 'idle', 'requesting', 'active', 'error'

    const processAndSendFrame = async (screenCanvas, cameraCanvas) => {
        try {
            setIsProcessing(true);
            // MODIFIED: Now includes both screen and camera data
            const screenData = screenCanvas.toDataURL('image/jpeg', 0.8);
            const cameraData = cameraCanvas ? cameraCanvas.toDataURL('image/jpeg', 0.8) : null;

            const payload = {
                timestamp: new Date().toISOString(),
                screenImageData: screenData,
                cameraImageData: cameraData, // ADDED: Camera data in payload
                screenWidth: screenCanvas.width,
                screenHeight: screenCanvas.height
            };

            const response = await fetch('http://localhost:5000/screenshot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Failed to process screen and camera data');
            }

            const result = await response.json();
            setLastProcessed({
                timestamp: new Date().toLocaleTimeString(),
                recommendation: result.recommendation
            });
            setStatus('active');

        } catch (err) {
            console.error('Error processing data:', err);
            setError('Failed to process data. Please try again.');
            setStatus('error');
        } finally {
            setIsProcessing(false);
        }
    };

    // ADDED: New function to start camera capture
    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            });
            setCameraStream(mediaStream);
        } catch (err) {
            console.error('Error accessing camera:', err);
            setError('Camera permission denied. Please try again.');
        }
    };

    const startCapture = async () => {
        try {
            setError(null);
            setStatus('requesting');

            // MODIFIED: Now starts both screen and camera capture
            const screenMediaStream = await navigator.mediaDevices.getDisplayMedia({
                video: {
                    cursor: 'never'
                },
                audio: false
            });

            await startCamera(); // ADDED: Start camera capture

            setScreenStream(screenMediaStream);
            setIsCapturing(true);
            setStatus('active');

            screenMediaStream.getVideoTracks()[0].addEventListener('ended', () => {
                stopCapture();
            });
        } catch (err) {
            console.error('Error accessing screen or camera:', err);
            setError('Permission denied or capture cancelled. Please try again.');
            setStatus('error');
            setIsCapturing(false);
        }
    };

    useEffect(() => {
        if (isCapturing) {
            setSpinning(true);
        } else {
            setSpinning(false);
        }
    }, [isCapturing]);

    const stopCapture = () => {
        // MODIFIED: Stop both screen and camera streams
        if (screenStream) {
            screenStream.getTracks().forEach(track => track.stop());
            setScreenStream(null);
        }
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            setCameraStream(null);
        }
        setIsCapturing(false);
        setLastProcessed(null);
        setStatus('idle');
    };

    useEffect(() => {
        let intervalId;

        if (isCapturing && screenStream) {
            intervalId = setInterval(() => {
                // MODIFIED: Process both screen and camera frames
                const screenVideo = document.createElement('video');
                screenVideo.srcObject = screenStream;

                screenVideo.onloadedmetadata = () => {
                    const screenCanvas = document.createElement('canvas');
                    screenCanvas.width = screenVideo.videoWidth;
                    screenCanvas.height = screenVideo.videoHeight;

                    const screenCtx = screenCanvas.getContext('2d');
                    screenCtx.drawImage(screenVideo, 0, 0);

                    // ADDED: Process camera frame if available
                    if (cameraStream) {
                        const cameraVideo = document.createElement('video');
                        cameraVideo.srcObject = cameraStream;
                        cameraVideo.onloadedmetadata = () => {
                            const cameraCanvas = document.createElement('canvas');
                            cameraCanvas.width = cameraVideo.videoWidth;
                            cameraCanvas.height = cameraVideo.videoHeight;

                            const cameraCtx = cameraCanvas.getContext('2d');
                            cameraCtx.drawImage(cameraVideo, 0, 0);

                            processAndSendFrame(screenCanvas, cameraCanvas);

                            cameraVideo.remove();
                            cameraCanvas.remove();
                        };
                        cameraVideo.play();
                    } else {
                        processAndSendFrame(screenCanvas, null);
                    }

                    screenVideo.remove();
                    screenCanvas.remove();
                };

                screenVideo.play();
            }, 8000);
        }

        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [isCapturing, screenStream, cameraStream]); // MODIFIED: Added cameraStream dependency

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