import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import DriverCard from '../components/DriverCard'
import driverStats from '../data/driver_stats.json'
import { getDriverImage } from '../data/drivers'

function AllTimePeak() {
    const [sortBy, setSortBy] = useState('peak_elo')
    const [searchQuery, setSearchQuery] = useState('')
    const [showAll, setShowAll] = useState(false)

    // Convert stats object to array with name
    const allDrivers = useMemo(() => {
        return Object.entries(driverStats).map(([name, stats]) => ({
            name,
            ...stats
        }))
    }, [])

    // Filter and sort drivers
    const displayedDrivers = useMemo(() => {
        let filtered = allDrivers

        // Apply search filter
        if (searchQuery) {
            filtered = filtered.filter(d =>
                d.name.toLowerCase().includes(searchQuery.toLowerCase())
            )
        }

        // Sort based on selected criteria
        switch (sortBy) {
            case 'peak_elo':
                filtered = filtered.sort((a, b) => b.peak_elo - a.peak_elo)
                break
            case 'avg_elo':
                filtered = filtered.sort((a, b) => b.avg_elo - a.avg_elo)
                break
            case 'wins':
                filtered = filtered.sort((a, b) => b.wins - a.wins)
                break
            case 'races':
                filtered = filtered.sort((a, b) => b.total_races - a.total_races)
                break
            case 'name':
                filtered = filtered.sort((a, b) => a.name.localeCompare(b.name))
                break
            default:
                break
        }

        // Limit display unless showAll is true
        return showAll ? filtered : filtered.slice(0, 50)
    }, [allDrivers, sortBy, searchQuery, showAll])

    // Get label for sort option
    const getSortLabel = () => {
        switch (sortBy) {
            case 'peak_elo': return 'Peak ELO'
            case 'avg_elo': return 'Average ELO'
            case 'wins': return 'Race Wins'
            case 'races': return 'Total Races'
            case 'name': return 'Alphabetical'
            default: return 'Peak ELO'
        }
    }

    return (
        <main className="section" style={{ paddingTop: '120px' }}>
            <div className="container">
                <motion.div
                    className="section-header"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <h1 className="section-title text-gradient">All-Time Leaderboard</h1>
                    <p className="section-subtitle">
                        {allDrivers.length} drivers ranked by {getSortLabel()}
                    </p>
                </motion.div>

                {/* Filter Controls */}
                <motion.div
                    className="glass-card"
                    style={{
                        padding: 'var(--spacing-md)',
                        marginBottom: 'var(--spacing-xl)',
                        display: 'flex',
                        flexWrap: 'wrap',
                        gap: 'var(--spacing-md)',
                        alignItems: 'center'
                    }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    {/* Search Input */}
                    <div style={{ flex: '1 1 250px' }}>
                        <input
                            type="text"
                            placeholder="Search drivers..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '12px 16px',
                                background: 'var(--bg-glass)',
                                border: '1px solid var(--border-glass)',
                                borderRadius: 'var(--radius-md)',
                                color: 'var(--text-primary)',
                                fontSize: '1rem'
                            }}
                        />
                    </div>

                    {/* Sort Buttons */}
                    <div style={{
                        display: 'flex',
                        gap: 'var(--spacing-xs)',
                        flexWrap: 'wrap',
                        flex: '1 1 auto'
                    }}>
                        <span style={{ color: 'var(--text-secondary)', alignSelf: 'center', marginRight: '8px' }}>
                            Sort by:
                        </span>
                        {[
                            { key: 'peak_elo', label: 'Peak ELO' },
                            { key: 'avg_elo', label: 'Avg ELO' },
                            { key: 'wins', label: 'Wins' },
                            { key: 'races', label: 'Races' },
                            { key: 'name', label: 'A-Z' }
                        ].map(opt => (
                            <button
                                key={opt.key}
                                onClick={() => setSortBy(opt.key)}
                                style={{
                                    padding: '8px 16px',
                                    background: sortBy === opt.key ? 'var(--accent-primary)' : 'var(--bg-glass)',
                                    border: '1px solid var(--border-glass)',
                                    borderRadius: 'var(--radius-sm)',
                                    color: sortBy === opt.key ? '#fff' : 'var(--text-secondary)',
                                    cursor: 'pointer',
                                    fontSize: '0.9rem',
                                    transition: 'all 0.2s'
                                }}
                            >
                                {opt.label}
                            </button>
                        ))}
                    </div>
                </motion.div>

                {/* Driver Grid */}
                <div className="driver-grid">
                    {displayedDrivers.map((driver, index) => (
                        <DriverCard
                            key={driver.name}
                            driver={{
                                name: driver.name,
                                elo: sortBy === 'peak_elo' ? driver.peak_elo :
                                    sortBy === 'avg_elo' ? driver.avg_elo :
                                        sortBy === 'wins' ? driver.wins :
                                            sortBy === 'races' ? driver.total_races :
                                                driver.peak_elo
                            }}
                            index={index}
                            subtitle={sortBy === 'wins' ? 'wins' : sortBy === 'races' ? 'races' : null}
                        />
                    ))}
                </div>

                {/* Show More Button */}
                {!showAll && displayedDrivers.length >= 50 && !searchQuery && (
                    <motion.div
                        style={{ textAlign: 'center', marginTop: 'var(--spacing-xl)' }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <button
                            onClick={() => setShowAll(true)}
                            style={{
                                padding: '14px 32px',
                                background: 'var(--gradient-primary)',
                                border: 'none',
                                borderRadius: 'var(--radius-md)',
                                color: '#fff',
                                fontSize: '1rem',
                                fontWeight: 600,
                                cursor: 'pointer',
                                transition: 'transform 0.2s, box-shadow 0.2s'
                            }}
                            onMouseEnter={(e) => {
                                e.target.style.transform = 'scale(1.05)'
                                e.target.style.boxShadow = '0 10px 30px rgba(255, 30, 30, 0.3)'
                            }}
                            onMouseLeave={(e) => {
                                e.target.style.transform = 'scale(1)'
                                e.target.style.boxShadow = 'none'
                            }}
                        >
                            Show All {allDrivers.length} Drivers
                        </button>
                    </motion.div>
                )}

                {/* No Results */}
                {displayedDrivers.length === 0 && (
                    <motion.div
                        className="glass-card"
                        style={{
                            padding: 'var(--spacing-xl)',
                            textAlign: 'center',
                            color: 'var(--text-secondary)'
                        }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <p style={{ fontSize: '1.2rem' }}>
                            No drivers found matching "{searchQuery}"
                        </p>
                    </motion.div>
                )}
            </div>
        </main>
    )
}

export default AllTimePeak
