import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { allTimePeakElo, currentGrid2025, getDriverImage } from '../data/drivers'

// Helper to get plot path from driver name
const getDriverPlotPath = (name) => {
    const filename = name
        .replace(/ /g, '_')
        .replace(/é/g, 'e')
        .replace(/ö/g, 'o')
        .replace(/ü/g, 'u')
        .replace(/á/g, 'a')
        .replace(/í/g, 'i')
        .replace(/ó/g, 'o')
        .replace(/ñ/g, 'n')
        .replace(/-/g, '');
    return `/plots/${filename}.png`;
}

function DriverDetail() {
    const { name } = useParams()
    const navigate = useNavigate()
    const decodedName = decodeURIComponent(name)
    const [showEloHistory, setShowEloHistory] = useState(false)

    // Find driver in both lists
    const allTimeDriver = allTimePeakElo.find(d => d.name === decodedName)
    const currentGridDriver = currentGrid2025.find(d => d.name === decodedName)

    // Use whichever data we have, prefer current grid if available
    const driver = currentGridDriver || allTimeDriver

    if (!driver) {
        return (
            <main className="driver-detail">
                <div className="container">
                    <button onClick={() => navigate(-1)} className="back-button">
                        ← Back
                    </button>
                    <h1>Driver not found</h1>
                </div>
            </main>
        )
    }

    // Full Screen ELO History View
    if (showEloHistory) {
        return (
            <main className="elo-history-view">
                <motion.div
                    className="elo-history-container"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.4 }}
                >
                    <motion.button
                        onClick={() => setShowEloHistory(false)}
                        className="back-button elo-back-button"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3 }}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        ← Back to Profile
                    </motion.button>
                    <motion.h2
                        className="elo-history-title"
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4, delay: 0.1 }}
                    >
                        {driver.name} — ELO History
                    </motion.h2>
                    <motion.div
                        className="elo-plot-wrapper"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        <img
                            src={getDriverPlotPath(driver.name)}
                            alt={`${driver.name} ELO History`}
                            className="elo-plot-image"
                            onError={(e) => {
                                e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400"><rect fill="%23111" width="800" height="400"/><text x="400" y="200" font-size="24" text-anchor="middle" fill="%23666">No ELO history available</text></svg>'
                            }}
                        />
                    </motion.div>
                </motion.div>
            </main>
        )
    }

    return (
        <main className="driver-detail">
            <div className="container">
                <motion.button
                    onClick={() => navigate(-1)}
                    className="back-button"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4 }}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                >
                    ← Back to Rankings
                </motion.button>

                <motion.div
                    className="driver-detail-header"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                >
                    <motion.img
                        src={getDriverImage(driver.name)}
                        alt={driver.name}
                        className="driver-detail-image"
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        onError={(e) => {
                            e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23333" width="100" height="100"/><text x="50" y="55" font-size="40" text-anchor="middle" fill="%23666">?</text></svg>'
                        }}
                    />
                    <div className="driver-detail-info">
                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.3 }}
                        >
                            {driver.name}
                        </motion.h1>
                        <motion.div
                            className="driver-detail-elo text-elo"
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.5, delay: 0.4 }}
                        >
                            {driver.elo}
                        </motion.div>
                        <motion.p
                            className="driver-detail-rank"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.5, delay: 0.5 }}
                        >
                            {currentGridDriver && `2025 Grid Rank: #${currentGridDriver.rank}`}
                            {currentGridDriver && allTimeDriver && ' • '}
                            {allTimeDriver && `All-Time Peak Rank: #${allTimeDriver.rank}`}
                        </motion.p>
                    </div>
                </motion.div>

                {/* View ELO History Button */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.55 }}
                    style={{ marginTop: '2rem', marginBottom: '2rem' }}
                >
                    <motion.button
                        onClick={() => setShowEloHistory(true)}
                        className="elo-history-button"
                        whileHover={{ scale: 1.03 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        📈 View ELO History
                    </motion.button>
                </motion.div>

                {/* Stats Cards */}
                <motion.div
                    className="nav-cards"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                >
                    {allTimeDriver && (
                        <div className="nav-card" style={{ cursor: 'default' }}>
                            <h3 className="nav-card-title" style={{ color: 'var(--accent-gold)' }}>
                                All-Time Peak ELO
                            </h3>
                            <p className="nav-card-description">
                                Peak Rating: <strong style={{ fontSize: '1.5rem', color: 'var(--text-primary)' }}>{allTimeDriver.elo}</strong>
                            </p>
                            <p className="nav-card-description">
                                Historical Rank: #{allTimeDriver.rank} of 700+ drivers
                            </p>
                        </div>
                    )}
                    {currentGridDriver && (
                        <div className="nav-card" style={{ cursor: 'default' }}>
                            <h3 className="nav-card-title" style={{ color: 'var(--accent-blue)' }}>
                                2025 Grid Standing
                            </h3>
                            <p className="nav-card-description">
                                Current ELO: <strong style={{ fontSize: '1.5rem', color: 'var(--text-primary)' }}>{currentGridDriver.elo}</strong>
                            </p>
                            <p className="nav-card-description">
                                Grid Position: #{currentGridDriver.rank} of 21 drivers
                            </p>
                        </div>
                    )}
                </motion.div>
            </div>
        </main>
    )
}

export default DriverDetail
