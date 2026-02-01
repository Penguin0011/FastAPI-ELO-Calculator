import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import timelineData from '../data/timeline_data.json'
import { getDriverImage } from '../data/drivers'

function Timeline() {
    const years = useMemo(() => Object.keys(timelineData).map(Number).sort((a, b) => a - b), [])
    const [selectedYear, setSelectedYear] = useState(years[years.length - 1] || 2025)

    const rankings = useMemo(() => {
        return timelineData[String(selectedYear)] || []
    }, [selectedYear])

    // Get era description
    const getEraDescription = (year) => {
        if (year >= 2022) return "Ground Effect Era"
        if (year >= 2014) return "Turbo Hybrid Era"
        if (year >= 2009) return "Aerodynamic Regulations Era"
        if (year >= 2006) return "V8 Era"
        if (year >= 2000) return "Schumacher Dominance"
        if (year >= 1994) return "Safety Revolution Era"
        if (year >= 1989) return "Semi-Automatic Era"
        if (year >= 1977) return "Ground Effect Era (Original)"
        if (year >= 1966) return "3.0L Era"
        if (year >= 1961) return "1.5L Formula"
        if (year >= 1958) return "Rear-Engine Revolution"
        return "Front-Engine Era"
    }

    return (
        <main className="section" style={{ paddingTop: '120px', minHeight: '100vh' }}>
            <div className="container">
                <motion.div
                    className="section-header"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <h1 className="section-title text-gradient">Historical Timeline</h1>
                    <p className="section-subtitle">
                        Explore how driver rankings evolved throughout F1 history
                    </p>
                </motion.div>

                {/* Year Slider */}
                <motion.div
                    className="glass-card"
                    style={{ padding: 'var(--spacing-lg)', marginBottom: 'var(--spacing-xl)' }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--spacing-md)' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>{years[0]}</span>
                        <div style={{ textAlign: 'center' }}>
                            <span style={{
                                fontSize: '3rem',
                                fontWeight: 700,
                                color: 'var(--accent-primary)',
                                textShadow: '0 0 30px rgba(255, 30, 30, 0.3)'
                            }}>
                                {selectedYear}
                            </span>
                            <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
                                {getEraDescription(selectedYear)}
                            </p>
                        </div>
                        <span style={{ color: 'var(--text-secondary)' }}>{years[years.length - 1]}</span>
                    </div>
                    <input
                        type="range"
                        min={years[0]}
                        max={years[years.length - 1]}
                        value={selectedYear}
                        onChange={(e) => setSelectedYear(Number(e.target.value))}
                        style={{
                            width: '100%',
                            height: '8px',
                            borderRadius: '4px',
                            background: `linear-gradient(to right, var(--accent-primary) 0%, var(--accent-primary) ${((selectedYear - years[0]) / (years[years.length - 1] - years[0])) * 100}%, var(--bg-glass) ${((selectedYear - years[0]) / (years[years.length - 1] - years[0])) * 100}%, var(--bg-glass) 100%)`,
                            appearance: 'none',
                            cursor: 'pointer'
                        }}
                    />
                    {/* Quick Jump Buttons */}
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        gap: 'var(--spacing-xs)',
                        marginTop: 'var(--spacing-md)',
                        flexWrap: 'wrap'
                    }}>
                        {[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025].filter(y => years.includes(y)).map(year => (
                            <button
                                key={year}
                                onClick={() => setSelectedYear(year)}
                                style={{
                                    padding: '6px 12px',
                                    background: selectedYear === year ? 'var(--accent-primary)' : 'var(--bg-glass)',
                                    border: '1px solid var(--border-glass)',
                                    borderRadius: 'var(--radius-sm)',
                                    color: selectedYear === year ? '#fff' : 'var(--text-secondary)',
                                    cursor: 'pointer',
                                    fontSize: '0.85rem',
                                    transition: 'all 0.2s'
                                }}
                            >
                                {year}
                            </button>
                        ))}
                    </div>
                </motion.div>

                {/* Rankings List */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                >
                    <h2 style={{ marginBottom: 'var(--spacing-md)' }}>
                        Top Drivers at End of {selectedYear}
                    </h2>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)' }}>
                        {rankings.slice(0, 20).map((driver, index) => (
                            <motion.div
                                key={driver.name}
                                className="glass-card"
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    padding: 'var(--spacing-sm) var(--spacing-md)',
                                    gap: 'var(--spacing-md)'
                                }}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.3, delay: index * 0.03 }}
                            >
                                {/* Rank */}
                                <span style={{
                                    width: '40px',
                                    fontWeight: 700,
                                    fontSize: '1.2rem',
                                    color: index === 0 ? 'var(--accent-gold)' :
                                        index === 1 ? 'var(--accent-silver)' :
                                            index === 2 ? 'var(--accent-bronze)' : 'var(--text-secondary)'
                                }}>
                                    #{index + 1}
                                </span>

                                {/* Driver Image */}
                                <img
                                    src={getDriverImage(driver.name)}
                                    alt={driver.name}
                                    style={{
                                        width: '48px',
                                        height: '48px',
                                        borderRadius: '50%',
                                        objectFit: 'cover',
                                        border: '2px solid var(--border-glass)'
                                    }}
                                    onError={(e) => e.target.src = '/drivers/default.png'}
                                />

                                {/* Name */}
                                <Link
                                    to={`/driver/${encodeURIComponent(driver.name)}`}
                                    style={{
                                        flex: 1,
                                        fontWeight: 500,
                                        transition: 'color 0.2s'
                                    }}
                                    onMouseEnter={(e) => e.target.style.color = 'var(--accent-primary)'}
                                    onMouseLeave={(e) => e.target.style.color = 'var(--text-primary)'}
                                >
                                    {driver.name}
                                </Link>

                                {/* ELO */}
                                <span className="text-elo" style={{
                                    fontSize: '1.3rem',
                                    color: 'var(--accent-primary)',
                                    textShadow: '0 0 15px rgba(255, 30, 30, 0.2)'
                                }}>
                                    {driver.elo}
                                </span>
                            </motion.div>
                        ))}
                    </div>

                    {rankings.length > 20 && (
                        <p style={{
                            textAlign: 'center',
                            color: 'var(--text-secondary)',
                            marginTop: 'var(--spacing-md)'
                        }}>
                            + {rankings.length - 20} more drivers
                        </p>
                    )}
                </motion.div>
            </div>
        </main>
    )
}

export default Timeline
