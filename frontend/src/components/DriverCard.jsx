import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { getDriverImage } from '../data/drivers'

function DriverCard({ driver, index, subtitle }) {
    // Use driver.rank if available, otherwise use index + 1
    const rank = driver.rank || (index + 1)
    const rankClass = rank === 1 ? 'top-1' : rank === 2 ? 'top-2' : rank === 3 ? 'top-3' : ''

    return (
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{
                duration: 0.5,
                delay: (index % 12) * 0.08,
                ease: [0.25, 0.46, 0.45, 0.94]
            }}
            viewport={{ once: true, margin: "-50px" }}
        >
            <Link to={`/driver/${encodeURIComponent(driver.name)}`}>
                <div className="driver-card glass-card">
                    <span className={`driver-card-rank ${rankClass}`}>#{rank}</span>
                    <img
                        src={getDriverImage(driver.name)}
                        alt={driver.name}
                        className="driver-card-image"
                        onError={(e) => {
                            e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23333" width="100" height="100"/><text x="50" y="55" font-size="40" text-anchor="middle" fill="%23666">?</text></svg>'
                        }}
                    />
                    <h3 className="driver-card-name">{driver.name}</h3>
                    <div className="driver-card-elo text-elo">
                        {driver.elo}
                        {subtitle && <span style={{ fontSize: '0.7em', opacity: 0.7, marginLeft: '4px' }}>{subtitle}</span>}
                    </div>
                </div>
            </Link>
        </motion.div>
    )
}

export default DriverCard

