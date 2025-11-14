import React, { useState } from 'react';
import SignIn from './SignIn';
import SignUp from './SignUp';
import ResumeAnalyzer from './ResumeAnalyzer';

function App() {
  const [page, setPage] = useState('signIn');
  const [user, setUser] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      {page === 'signIn' && (
        <SignIn onSignIn={userData => { setUser(userData); setPage('analyze'); }} onGoToSignUp={() => setPage('signUp')} />
      )}
      {page === 'signUp' && (
        <SignUp onSignUp={userData => { setUser(userData); setPage('analyze'); }} onGoToSignIn={() => setPage('signIn')} />
      )}
      {page === 'analyze' && (
        <ResumeAnalyzer user={user} onSignOut={() => { setUser(null); setPage('signIn'); }} />
      )}
    </div>
  );
}

export default App;
