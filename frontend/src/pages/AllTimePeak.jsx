import { motion } from 'framer-motion'
import { allTimePeakElo } from '../data/drivers'
import DriverCard from '../components/DriverCard'

function AllTimePeak() {
    return (
        <main className="section" style={{ paddingTop: '120px' }}>
            <div className="container">
                <motion.div
                    className="section-header"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <h1 className="section-title text-gradient">All-Time Peak ELO</h1>
                    <p className="section-subtitle">
                        The greatest drivers in F1 history, ranked by their highest career ELO rating
                    </p>
                </motion.div>

                <div className="driver-grid">
                    {allTimePeakElo.map((driver, index) => (
                        <DriverCard key={driver.name} driver={driver} index={index} />
                    ))}
                </div>
            </div>
        </main>
    )
}

export default AllTimePeak
