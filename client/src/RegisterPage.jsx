import { useState } from 'react';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear error when user starts typing
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic validation
    if (!formData.username || !formData.password || !formData.confirmPassword) {
      setError('All fields are required');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    try {
      // Placeholder for API call
      console.log('Registering with:', {
        username: formData.username,
        password: formData.password
      });
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('Registration successful!');
      
      // Clear form
      setFormData({
        username: '',
        password: '',
        confirmPassword: ''
      });
    } catch (error) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="w-full min-h-screen bg-black flex items-center justify-center">
      <div className="w-full max-w-lg px-6 py-8">
        <div className="relative">
          {/* Outer glow container */}
          <div className="absolute inset-0 bg-cyan-300 opacity-20 blur-xl animate-pulse rounded-2xl"></div>
          
          {/* Main container */}
          <div className="relative bg-black border border-cyan-300 rounded-2xl p-12 shadow-2xl shadow-cyan-300/30">
            <h1 className="text-5xl font-bold text-cyan-300 text-center mb-12 animate-glow tracking-wider">
              REGISTER
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

              <div>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirm Password"
                  className="w-full bg-black border border-cyan-300 rounded-xl p-4 text-cyan-300 placeholder-cyan-300/40 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:border-transparent transition-all hover:shadow-lg hover:shadow-cyan-300/20"
                />
              </div>
              
              {error && (
                <div className="text-red-400 text-center animate-pulse">
                  {error}
                </div>
              )}
              
              <button
                type="submit"
                className="w-full bg-cyan-300 text-black font-bold py-4 px-6 rounded-xl hover:bg-cyan-200 transition-all duration-300 hover:shadow-lg hover:shadow-cyan-300/50 active:transform active:scale-95 text-lg"
              >
                Create Account
              </button>
            </form>
            
            <div className="mt-8 text-center">
              <a href="#" className="text-cyan-300 hover:text-cyan-200 transition-colors text-lg">
                Already have an account? Login
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;