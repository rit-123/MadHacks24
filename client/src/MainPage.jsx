import React from 'react';

const GlowingCirclePattern = () => {
  const totalBlocks = 24;
  const radius = 140;
  const blocks = Array.from({ length: totalBlocks }).map((_, i) => {
    const angle = (i * 360) / totalBlocks;
    return {
      angle,
      color: i % 3 === 0 ? '#7FFFD4' : '#87CEFA',
      size: i % 3 === 0 ? 24 : 32,
    };
  });

  return (
    <div className="w-full h-96 bg-black flex items-center justify-center relative">
      <svg width="0" height="0">
        <defs>
          <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
      </svg>

      {/* Fixed center container */}
      <div className="absolute inset-0 flex items-center justify-center">
        {/* Rotating blocks container */}
        <div 
          className="relative w-96 h-96 animate-spin"
          style={{ 
            animationDuration: '10s',
            transformOrigin: 'center center'
          }}
        >
          {blocks.map((block, index) => (
            <div
              key={index}
              className="absolute"
              style={{
                left: '50%',
                top: '50%',
                width: `${block.size}px`,
                height: `${block.size}px`,
                transform: `
                  translate(-50%, -50%) 
                  rotate(${block.angle}deg) 
                  translateY(-${radius}px) 
                  rotate(-${block.angle}deg)
                `,
                filter: 'url(#glow)',
              }}
            >
              <div
                className="w-full h-full rounded-sm"
                style={{
                  backgroundColor: block.color,
                  boxShadow: `0 0 20px ${block.color}`,
                }}
              />
            </div>
          ))}
        </div>

        {/* Centered text and button that stays still */}
        <div className="absolute flex flex-col items-center justify-center gap-8">
          <div className="flex flex-col items-center">
            <span 
              className="text-3xl" 
              style={{ 
                textShadow: '0 0 10px #87CEFA',
                fontFamily: 'Arial Black, sans-serif',
                letterSpacing: '-0.05em',
                fontStretch: 'condensed',
                fontWeight: 900,
                WebkitTextStroke: '1px white',
                WebkitTextFillColor: 'white',
                textRendering: 'geometricPrecision'
              }}
            >
              LISTEN
            </span>
            <span 
              className="text-3xl" 
              style={{ 
                textShadow: '0 0 10px #87CEFA',
                fontFamily: 'Arial Black, sans-serif',
                letterSpacing: '-0.05em',
                fontStretch: 'condensed',
                fontWeight: 900,
                WebkitTextStroke: '1px white',
                WebkitTextFillColor: 'white',
                textRendering: 'geometricPrecision'
              }}
            >
              TUAH
            </span>
          </div>
          
          {/* Start Button */}
          <button 
            className="px-8 py-2 rounded-md transition-all duration-300 hover:scale-105"
            style={{
              backgroundColor: 'transparent',
              border: '2px solid white',
              color: 'white',
              fontFamily: 'Arial Black, sans-serif',
              letterSpacing: '0.05em',
              fontWeight: 900,
              textShadow: '0 0 10px #87CEFA',
              boxShadow: '0 0 20px #87CEFA',
              filter: 'url(#glow)',
            }}
          >
            START
          </button>
        </div>
      </div>
    </div>
  );
};

export default GlowingCirclePattern;