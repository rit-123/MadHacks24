import React from 'react';
import SpotifyConnector from './SpotifyConnector';
import ScreenAnalyzer from './ScreenAnalyzer';
import { useState, useEffect } from 'react';
import { useSearchParams  } from 'react-router-dom';
import axios from 'axios';


const GlowingCirclePattern = () => {
    const blocks = [];
    const totalBlocks = 24;
    const radius = 220;
    const [spinning, setSpinning] = useState(false);
    const [searchParams, setSearchParams] = useSearchParams();
    try {
        const key = searchParams.get('code');
        try {
            axios.post('http://localhost:5000/spotify', {code: key});
        } catch (error) {
            console.log(error);
        }
    } catch (error) {}

    for (let i = 0; i < totalBlocks; i++) {
        const angle = (i / totalBlocks) * Math.PI * 2;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        const isGreen = i % 3 === 2;

        blocks.push({
            x,
            y,
            color: isGreen ? '#98FFB3' : '#87CEFA',
            size: isGreen ? 32 : 45
        });
    }


    return (
        <>
            <style>
                {`
          .spin {
            animation: spin 20s linear infinite;
          }
          
          .pulse {
            animation: pulse 2.5s infinite;
          }
          
          .spin-and-pulse {
            animation: spin 20s linear infinite, pulse 2.5s  infinite;
          }
          
          @keyframes spin {
            from {
              transform: rotate(0deg);
            }
            to {
              transform: rotate(360deg);
            }
          }
          
          @keyframes pulse {
            0% {
              transform: scale(1) rotate(0deg);
            }
            50% {
              transform: scale(1.1) rotate(180deg);
            }
            100% {
              transform: scale(1) rotate(360deg);
            }
          }
        `}
            </style>

            <div className="w-full h-screen bg-black flex items-center justify-center">
                <div className="relative w-[700px] h-[700px]">
                    <div className={`${spinning ? 'spin-and-pulse':''} absolute inset-0`}>
                        {blocks.map((block, index) => (
                            <div
                                key={index}
                                style={{
                                    position: 'absolute',
                                    left: '50%',
                                    top: '50%',
                                    width: `${block.size}px`,
                                    height: `${block.size}px`,
                                    transform: `translate(-50%, -50%) translate(${block.x}px, ${block.y}px)`,
                                    backgroundColor: block.color,
                                    boxShadow: `0 0 30px ${block.color}`,
                                    filter: 'brightness(1.2) blur(1px)',
                                    borderRadius: '8px',
                                }}
                            />
                        ))}
                    </div>

                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <div
                            style={{
                                fontFamily: 'Arial Black, sans-serif',
                                letterSpacing: '-0.05em',
                                textShadow: '0 0 10px rgba(255, 255, 255, 0.8)',
                                filter: 'brightness(1.2)',
                                fontSize: '65px',
                                lineHeight: '1.2',
                                display: 'flex',
                                flexDirection: 'column',
                                alignItems: 'center',
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                textAlign: 'center',
                            }}
                        >
                            <div style={{marginTop:"100px"}}>
                                <div className="text-white font-black mb-3">LISTEN TUAH</div>
                                <ScreenAnalyzer setSpinning={setSpinning}/>
                            </div>
                        </div>
                    </div>
                </div>
                
                
            </div>
        </>
    );
};

export default GlowingCirclePattern;