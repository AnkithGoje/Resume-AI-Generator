import { useState, type ReactNode } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import { ResumeForm } from './components/ResumeForm';
import { AnalysisResultDisplay } from './components/AnalysisResultDisplay';
import type { AnalysisResult } from './types';

function Dashboard() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { token } = useAuth();

  const handleAnalysis = async (formData: FormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/analyze-resume`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        },
      });
      setResult(response.data);
    } catch (err: any) {
      console.error(err);
      if (err.response?.status === 403) {
        setError("Usage limit exceeded. You have reached the maximum of 50 resume analyses.");
      } else {
        setError(err.response?.data?.detail || "Something went wrong. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-16 md:py-24 max-w-5xl">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 mb-4">
          AI Resume Optimizer
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Transform your resume into a job-winning document with strict ATS-compliant formatting and strategic content enhancement.
        </p>
      </div>

      {error && (
        <div className="max-w-xl mx-auto mb-8 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-center justify-center">
          {error}
        </div>
      )}

      {!result ? (
        <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
          <ResumeForm onSubmit={handleAnalysis} isLoading={isLoading} />
        </div>
      ) : (
        <AnalysisResultDisplay result={result} onReset={() => setResult(null)} />
      )}
    </div>
  );
}

function PrivateRoute({ children }: { children: ReactNode }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

function App() {
  return (
    <AuthProvider>
      <Router future={{ v7_relativeSplatPath: true }}>
        <div className="min-h-screen bg-[#F8FAFC] bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]">
          <Navbar />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

