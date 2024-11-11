import React from 'react';
import axios from 'axios';

const SpotifyConnector = () => {
    const handleSpotifyConnect = async () => {
        try {
            const response = await axios.get('http://localhost:5000/connect_spotify');
            const url = response.data.url;
            console.log(url);
            window.open(url, '_blank');
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center px-6 py-8 bg-black">
            <div className="relative w-full max-w-lg">
                {/* Outer glow container */}
                <div className="absolute inset-0 bg-green-400 opacity-20 blur-xl animate-pulse rounded-2xl"></div>

                {/* Main container */}
                <div className="relative bg-black border border-green-400 rounded-2xl p-12 shadow-2xl shadow-green-400/30">
                    <h1 className="text-4xl font-bold text-green-400 text-center mb-8 animate-pulse tracking-wider">
                        Connect Your Spotify Account
                    </h1>

                    {/* Spotify Logo */}
                    <div className="flex justify-center mb-10">
                        <svg className="w-16 h-16 text-green-400" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                        </svg>
                    </div>

                    <button
                        onClick={handleSpotifyConnect}
                        className="w-full bg-green-400 text-black font-bold py-4 px-6 rounded-xl hover:bg-green-300 transition-all duration-300 hover:shadow-lg hover:shadow-green-400/50 active:transform active:scale-95 text-lg"
                    >
                        Connect with Spotify
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SpotifyConnector;