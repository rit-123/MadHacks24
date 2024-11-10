import React from 'react';

const GlowingCirclePattern = () => {
  const blocks = [];
  const totalBlocks = 24;
  const radius = 220;
  
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
            animation: spin 10s linear infinite;
          }
          
          @keyframes spin {
            from {
              transform: rotate(0deg);
            }
            to {
              transform: rotate(360deg);
            }
          }
        `}
      </style>

      <div className="w-full h-screen bg-black flex items-center justify-center">
        <div className="relative w-[700px] h-[700px]">
          <div className="spin absolute inset-0">
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
              <div className="text-white font-black mb-3">LISTEN</div>
              <div className="text-white font-black mb-32">TUAH</div>
              
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
                  marginTop:"18px"
                }}
              >
                START
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default GlowingCirclePattern;