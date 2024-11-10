import { useState } from 'react';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('Login successful!');
    } catch (error) {
      alert('Login failed!');
    }
  };

  return (
      <div className="w-full max-w-lg px-6 py-8">
        <div className="relative">
          {/* Outer glow container */}
          <div className="absolute inset-0 bg-cyan-300 opacity-20 blur-xl animate-pulse rounded-2xl"></div>
          
          {/* Main container */}
          <div className="relative bg-black border border-cyan-300 rounded-2xl p-12 shadow-2xl shadow-cyan-300/30">
            <h1 className="text-5xl font-bold text-cyan-300 text-center mb-12 animate-glow tracking-wider">
              LOGIN
            </h1>
            
            <form onSubmit={handleSubmit} className="space-y-8">
              <div>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Username"
                  className="w-full bg-black border border-cyan-300 rounded-xl p-4 text-cyan-300 placeholder-cyan-300/40 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:border-transparent transition-all hover:shadow-lg hover:shadow-cyan-300/20"
                />
              </div>
              
              <div>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Password"
                  className="w-full bg-black border border-cyan-300 rounded-xl p-4 text-cyan-300 placeholder-cyan-300/40 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:border-transparent transition-all hover:shadow-lg hover:shadow-cyan-300/20"
                />
              </div>
              
              <button
                type="submit"
                className="w-full bg-cyan-300 text-black font-bold py-4 px-6 rounded-xl hover:bg-cyan-200 transition-all duration-300 hover:shadow-lg hover:shadow-cyan-300/50 active:transform active:scale-95 text-lg"
              >
                Sign In
              </button>
            </form>
            
            <div className="mt-8 text-center">
              <a href="#" className="text-cyan-300 hover:text-cyan-200 transition-colors text-lg">
                Forgot Password?
              </a>
            </div>
          </div>
        </div>
      </div>
  );
};

export default LoginPage;