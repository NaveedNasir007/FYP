import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000';

function AdminLogin({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/token`, new URLSearchParams({
        username: email,
        password: password
      }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      onLogin(response.data.access_token);
    } catch (err) {
      setError('Login failed. Check credentials.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">RentEase Admin</h2>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="text"
              className="mt-1 block w-full border border-gray-300 rounded p-2"
              value={email} onChange={e => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              className="mt-1 block w-full border border-gray-300 rounded p-2"
              value={password} onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="w-full bg-teal-600 text-white p-2 rounded hover:bg-teal-700">Login</button>
        </form>
      </div>
    </div>
  );
}

function Dashboard({ token }) {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await axios.get(`${API_URL}/listings`);
        setListings(response.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchListings();
  }, []);

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Platform Overview</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded shadow border-t-4 border-teal-500">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Total Listings</h3>
          <p className="text-3xl font-bold mt-2">{listings.length}</p>
        </div>
        <div className="bg-white p-6 rounded shadow border-t-4 border-blue-500">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Active Users</h3>
          <p className="text-3xl font-bold mt-2">--</p>
        </div>
        <div className="bg-white p-6 rounded shadow border-t-4 border-yellow-500">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Pending Disputes</h3>
          <p className="text-3xl font-bold mt-2">0</p>
        </div>
      </div>

      <h2 className="text-xl font-bold mb-4">Recent Listings</h2>
      <div className="bg-white shadow rounded overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rate</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {listings.map(l => (
              <tr key={l.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{l.title}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{l.category}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${l.daily_rate}/day</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {l.status}
                  </span>
                </td>
              </tr>
            ))}
            {listings.length === 0 && (
              <tr>
                <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">No listings available.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('adminToken'));

  const handleLogin = (t) => {
    setToken(t);
    localStorage.setItem('adminToken', t);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('adminToken');
  };

  return (
    <BrowserRouter>
      {token && (
        <nav className="bg-gray-800 text-white p-4 flex justify-between items-center">
          <div className="font-bold text-xl tracking-wider">RentEase Admin</div>
          <button onClick={handleLogout} className="text-sm bg-gray-700 px-3 py-1 rounded hover:bg-gray-600">Logout</button>
        </nav>
      )}
      <Routes>
        <Route path="/login" element={!token ? <AdminLogin onLogin={handleLogin} /> : <Navigate to="/" />} />
        <Route path="/" element={token ? <Dashboard token={token} /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
