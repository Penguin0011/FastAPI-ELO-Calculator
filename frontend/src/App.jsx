import { Routes, Route } from 'react-router-dom'
import { ReactLenis } from '@studio-freight/react-lenis'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import AllTimePeak from './pages/AllTimePeak'
import CurrentGrid2025 from './pages/CurrentGrid2025'
import DriverDetail from './pages/DriverDetail'
import Compare from './pages/Compare'
import Timeline from './pages/Timeline'

function App() {
    return (
        <ReactLenis root>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/all-time" element={<AllTimePeak />} />
                <Route path="/2025" element={<CurrentGrid2025 />} />
                <Route path="/compare" element={<Compare />} />
                <Route path="/timeline" element={<Timeline />} />
                <Route path="/driver/:name" element={<DriverDetail />} />
            </Routes>
        </ReactLenis>
    )
}

export default App

