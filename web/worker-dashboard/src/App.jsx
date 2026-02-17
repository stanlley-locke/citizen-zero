import { BrowserRouter, Routes, Route } from 'react-router-dom';

function Dashboard() {
    return (
        <div className="p-10">
            <h1 className="text-4xl font-bold text-green-500">Worker Portal</h1>
            <p className="mt-4 text-xl">Welcome, Citizen.</p>
            <div className="mt-8 grid grid-cols-3 gap-4">
                <div className="p-6 bg-slate-800 rounded-lg border border-slate-700">
                    <h2 className="text-2xl font-bold">My Wallet</h2>
                    <p className="text-gray-400">View your Digital Credentials</p>
                </div>
                <div className="p-6 bg-slate-800 rounded-lg border border-slate-700">
                    <h2 className="text-2xl font-bold">Work History</h2>
                    <p className="text-gray-400">Track your employment</p>
                </div>
                <div className="p-6 bg-slate-800 rounded-lg border border-slate-700">
                    <h2 className="text-2xl font-bold">Profile</h2>
                    <p className="text-gray-400">Update contact info</p>
                </div>
            </div>
        </div>
    )
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
