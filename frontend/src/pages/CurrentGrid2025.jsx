import { motion } from 'framer-motion'
import { currentGrid2025 } from '../data/drivers'
import DriverCard from '../components/DriverCard'

function CurrentGrid2025() {
    return (
        <main className="section" style={{ paddingTop: '120px' }}>
            <div className="container">
                <motion.div
                    className="section-header"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <h1 className="section-title text-gradient">2025 Current Grid</h1>
                    <p className="section-subtitle">
                        Current F1 drivers ranked by their ELO rating at the end of the 2025 season
                    </p>
                </motion.div>

                <div className="driver-grid">
                    {currentGrid2025.map((driver, index) => (
                        <DriverCard key={driver.name} driver={driver} index={index} />
                    ))}
                </div>
            </div>
        </main>
    )
}

export default CurrentGrid2025
