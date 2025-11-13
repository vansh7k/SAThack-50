import React, { useState } from 'react';

export default function SignIn({ onSignIn, onGoToSignUp }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  function validatePassword(pass) {
    const hasUpper = /[A-Z]/.test(pass);
    const hasLower = /[a-z]/.test(pass);
    const hasNumber = /\d/.test(pass);
    const hasSpecial = /[!@#$%^&*()\-=_+;:'",.<>?]/.test(pass);
    const isValidLength = pass.length >= 8 && pass.length <= 16;
    
    return {
      isValid: hasUpper && hasLower && hasNumber && hasSpecial && isValidLength,
    };
  }

  const validation = validatePassword(password);

  function handleSubmit(e) {
    e.preventDefault();
    if (!email) {
      alert("Please enter email");
      return;
    }
    if (!validation.isValid) {
      alert("Invalid password format. Password must contain:\n- 8-16 characters\n- 1 uppercase letter\n- 1 lowercase letter\n- 1 number\n- 1 special character");
      return;
    }
    onSignIn({ email });
    setEmail('');
    setPassword('');
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-xl shadow-2xl w-96">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-blue-700 mb-2 text-center">SKILLBRIDGE</h2>
          <p className="text-sm text-center text-gray-600">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
            <input 
              type="email" 
              required 
              placeholder="your@email.com" 
              value={email}
              onChange={e => setEmail(e.target.value)} 
              className="w-full border-2 border-gray-300 p-3 rounded-lg focus:border-blue-500 focus:outline-none transition"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
            <div className="relative">
              <input 
                type={showPassword ? "text" : "password"} 
                required 
                placeholder="Enter your password" 
                value={password}
                onChange={e => setPassword(e.target.value)} 
                className="w-full border-2 border-gray-300 p-3 rounded-lg focus:border-blue-500 focus:outline-none transition"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-3 text-gray-600 hover:text-gray-800"
              >
                {showPassword ? "👁️" : "👁️‍🗨️"}
              </button>
            </div>
          </div>

          <button 
            className={`${
              validation.isValid && email 
                ? 'bg-blue-600 hover:bg-blue-700' 
                : 'bg-gray-400 cursor-not-allowed'
            } text-white font-bold py-3 px-4 rounded-lg transition duration-200 mt-2`}
            type="submit"
            disabled={!validation.isValid || !email}
          >
            Sign In
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <button 
              onClick={onGoToSignUp} 
              className="text-blue-600 font-semibold hover:underline cursor-pointer"
            >
              Sign Up
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
