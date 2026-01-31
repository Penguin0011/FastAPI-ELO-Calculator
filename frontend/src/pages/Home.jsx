import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { allTimePeakElo, currentGrid2025, getDriverImage } from '../data/drivers'

function Home() {
    const allTimeLeader = allTimePeakElo[0]
    const currentLeader = currentGrid2025[0]

    return (
        <main>
            {/* Hero Section */}
            <section className="hero">
                <div className="container">
                    <motion.div
                        className="hero-content"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.8 }}
                    >
                        {/* All-Time Peak Leader */}
                        <motion.div
                            initial={{ opacity: 0, x: -50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8, delay: 0.2 }}
                        >
                            <Link to={`/driver/${encodeURIComponent(allTimeLeader.name)}`}>
                                <div className="hero-leader-card all-time">
                                    <div className="hero-leader-badge all-time">
                                        👑 All-Time Peak ELO Leader
                                    </div>
                                    <motion.img
                                        src={getDriverImage(allTimeLeader.name)}
                                        alt={allTimeLeader.name}
                                        className="hero-leader-image"
                                        whileHover={{ scale: 1.05 }}
                                        transition={{ type: "spring", stiffness: 300 }}
                                        onError={(e) => {
                                            e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23333" width="100" height="100"/><text x="50" y="55" font-size="40" text-anchor="middle" fill="%23666">?</text></svg>'
                                        }}
                                    />
                                    <h2 className="hero-leader-name">{allTimeLeader.name}</h2>
                                    <motion.div
                                        className="hero-leader-elo text-elo"
                                        initial={{ scale: 0.5 }}
                                        animate={{ scale: 1 }}
                                        transition={{ duration: 0.5, delay: 0.6 }}
                                    >
                                        {allTimeLeader.elo}
                                    </motion.div>
                                </div>
                            </Link>
                        </motion.div>

                        {/* 2025 Current Grid Leader */}
                        <motion.div
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8, delay: 0.4 }}
                        >
                            <Link to={`/driver/${encodeURIComponent(currentLeader.name)}`}>
                                <div className="hero-leader-card current">
                                    <div className="hero-leader-badge current">
                                        🏎️ 2025 Grid Leader
                                    </div>
                                    <motion.img
                                        src={getDriverImage(currentLeader.name)}
                                        alt={currentLeader.name}
                                        className="hero-leader-image"
                                        whileHover={{ scale: 1.05 }}
                                        transition={{ type: "spring", stiffness: 300 }}
                                        onError={(e) => {
                                            e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23333" width="100" height="100"/><text x="50" y="55" font-size="40" text-anchor="middle" fill="%23666">?</text></svg>'
                                        }}
                                    />
                                    <h2 className="hero-leader-name">{currentLeader.name}</h2>
                                    <motion.div
                                        className="hero-leader-elo text-elo"
                                        initial={{ scale: 0.5 }}
                                        animate={{ scale: 1 }}
                                        transition={{ duration: 0.5, delay: 0.8 }}
                                    >
                                        {currentLeader.elo}
                                    </motion.div>
                                </div>
                            </Link>
                        </motion.div>
                    </motion.div>

                    {/* Navigation Cards */}
                    <motion.div
                        className="nav-cards"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.6 }}
                    >
                        <Link to="/all-time">
                            <div className="nav-card">
                                <h3 className="nav-card-title">All-Time Peak ELO</h3>
                                <p className="nav-card-description">
                                    Explore 700+ drivers ranked by their highest career ELO rating
                                </p>
                                <span className="nav-card-arrow">→</span>
                            </div>
                        </Link>
                        <Link to="/2025">
                            <div className="nav-card">
                                <h3 className="nav-card-title">2025 Current Grid</h3>
                                <p className="nav-card-description">
                                    See the complete 2025 season driver standings
                                </p>
                                <span className="nav-card-arrow">→</span>
                            </div>
                        </Link>
                    </motion.div>
                </div>
            </section>
        </main>
    )
}

export default Home
