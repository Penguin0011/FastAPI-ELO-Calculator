import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import driverStats from '../data/driver_stats.json'
import eloHistory from '../data/elo_history.json'

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

function Compare() {
    const [driver1, setDriver1] = useState('')
    const [driver2, setDriver2] = useState('')
    const [search1, setSearch1] = useState('')
    const [search2, setSearch2] = useState('')
    const [showDropdown1, setShowDropdown1] = useState(false)
    const [showDropdown2, setShowDropdown2] = useState(false)

    // Get all driver names sorted alphabetically
    const allDrivers = useMemo(() => {
        return Object.keys(driverStats).sort((a, b) => a.localeCompare(b))
    }, [])

    // Filter drivers based on search
    const filteredDrivers1 = useMemo(() => {
        if (!search1) return allDrivers.slice(0, 20)
        return allDrivers.filter(d =>
            d.toLowerCase().includes(search1.toLowerCase())
        ).slice(0, 15)
    }, [search1, allDrivers])

    const filteredDrivers2 = useMemo(() => {
        if (!search2) return allDrivers.slice(0, 20)
        return allDrivers.filter(d =>
            d.toLowerCase().includes(search2.toLowerCase())
        ).slice(0, 15)
    }, [search2, allDrivers])

    const stats1 = driver1 ? driverStats[driver1] : null
    const stats2 = driver2 ? driverStats[driver2] : null

    // Build Chart.js data from elo_history
    const chartData = useMemo(() => {
        if (!driver1 || !driver2) return null

        const history1 = eloHistory[driver1] || []
        const history2 = eloHistory[driver2] || []

        if (history1.length === 0 && history2.length === 0) return null

        // Find min and max race_index across both drivers
        const allIndices = [
            ...history1.map(h => h.race_index),
            ...history2.map(h => h.race_index)
        ]
        const minIdx = Math.min(...allIndices)
        const maxIdx = Math.max(...allIndices)

        // Create labels for X-axis (years at key points)
        const labels = []
        const labelMap = {}

            // Combine both histories to get year labels
            ;[...history1, ...history2].forEach(h => {
                if (!labelMap[h.race_index]) {
                    labelMap[h.race_index] = h.year
                }
            })

        // Generate labels for every 10th race index for readability
        for (let i = minIdx; i <= maxIdx; i++) {
            if (i % 50 === 0 || i === minIdx) {
                labels.push(labelMap[i] || '')
            } else {
                labels.push('')
            }
        }

        // Create data arrays with nulls for missing indices
        const createDataArray = (history) => {
            const dataMap = {}
            history.forEach(h => {
                dataMap[h.race_index] = h.rating
            })

            const result = []
            for (let i = minIdx; i <= maxIdx; i++) {
                result.push(dataMap[i] !== undefined ? dataMap[i] : null)
            }
            return result
        }

        return {
            labels: Array.from({ length: maxIdx - minIdx + 1 }, (_, i) => {
                const idx = minIdx + i
                // Only show year labels at intervals
                if (idx % 100 === 0 || idx === minIdx) {
                    return labelMap[idx] || ''
                }
                return ''
            }),
            datasets: [
                {
                    label: driver1,
                    data: createDataArray(history1),
                    borderColor: '#FF1E00',
                    backgroundColor: 'rgba(255, 30, 0, 0.2)',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1,
                    spanGaps: false
                },
                {
                    label: driver2,
                    data: createDataArray(history2),
                    borderColor: '#00F0FF',
                    backgroundColor: 'rgba(0, 240, 255, 0.2)',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1,
                    spanGaps: false
                }
            ]
        }
    }, [driver1, driver2])

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#fff',
                    font: { size: 14, family: 'Outfit, sans-serif' },
                    padding: 20
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: { size: 14, family: 'Space Grotesk, sans-serif' },
                bodyFont: { size: 13, family: 'Outfit, sans-serif' },
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
                padding: 12,
                callbacks: {
                    title: function (context) {
                        // Find the race name and year for this index
                        const dataIndex = context[0].dataIndex
                        const history1 = eloHistory[driver1] || []
                        const history2 = eloHistory[driver2] || []
                        const allHistory = [...history1, ...history2]
                        const minIdx = Math.min(...allHistory.map(h => h.race_index))
                        const targetIdx = minIdx + dataIndex

                        // Find entry for this race_index
                        const entry = allHistory.find(h => h.race_index === targetIdx)
                        return entry ? `${entry.race_name || 'Race ' + entry.round}, ${entry.year}` : ''
                    }
                }


            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                    drawBorder: false
                },
                ticks: {
                    color: '#a0a5b8',
                    font: { size: 11, family: 'Outfit, sans-serif' },
                    maxRotation: 0,
                    autoSkip: true,
                    maxTicksLimit: 10
                }
            },
            y: {
                min: 1000,
                max: 2500,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                    drawBorder: false
                },
                ticks: {
                    color: '#a0a5b8',
                    font: { size: 11, family: 'Outfit, sans-serif' },
                    stepSize: 250
                },
                title: {
                    display: true,
                    text: 'ELO Rating',
                    color: '#a0a5b8',
                    font: { size: 12, family: 'Outfit, sans-serif' }
                }
            }
        }
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
                    <h1 className="section-title text-gradient">Compare Drivers</h1>
                    <p className="section-subtitle">
                        Select two drivers to compare their ELO history and career statistics
                    </p>
                </motion.div>

                {/* Driver Selection */}
                <div className="compare-selection" style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: 'var(--spacing-lg)',
                    marginBottom: 'var(--spacing-xl)',
                    position: 'relative',
                    zIndex: 10
                }}>
                    {/* Driver 1 Selector */}
                    <motion.div
                        style={{
                            padding: 'var(--spacing-md)',
                            position: 'relative',
                            background: 'linear-gradient(145deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)',
                            backdropFilter: 'blur(16px)',
                            border: '1px solid var(--border-glass)',
                            borderRadius: 'var(--radius-lg)'
                        }}
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                    >
                        <label style={{ color: 'var(--accent-blue)', fontWeight: 600, marginBottom: '8px', display: 'block' }}>
                            Driver 1
                        </label>
                        <input
                            type="text"
                            value={driver1 || search1}
                            onChange={(e) => {
                                setSearch1(e.target.value)
                                setDriver1('')
                                setShowDropdown1(true)
                            }}
                            onFocus={() => setShowDropdown1(true)}
                            onBlur={() => setTimeout(() => setShowDropdown1(false), 200)}
                            placeholder="Search driver..."
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
                        <AnimatePresence>
                            {showDropdown1 && filteredDrivers1.length > 0 && (
                                <motion.div
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    style={{
                                        position: 'absolute',
                                        top: '100%',
                                        left: 0,
                                        right: 0,
                                        background: 'var(--bg-secondary)',
                                        border: '1px solid var(--border-glass)',
                                        borderRadius: 'var(--radius-md)',
                                        maxHeight: '300px',
                                        overflowY: 'auto',
                                        zIndex: 1000,
                                        boxShadow: '0 10px 40px rgba(0,0,0,0.5)'
                                    }}
                                >
                                    {filteredDrivers1.map(d => (
                                        <div
                                            key={d}
                                            onMouseDown={(e) => {
                                                e.preventDefault()
                                                setDriver1(d)
                                                setSearch1('')
                                                setShowDropdown1(false)
                                            }}
                                            style={{
                                                padding: '10px 16px',
                                                cursor: 'pointer',
                                                borderBottom: '1px solid var(--border-glass)',
                                                transition: 'background 0.2s'
                                            }}
                                            onMouseEnter={(e) => e.target.style.background = 'var(--bg-glass-hover)'}
                                            onMouseLeave={(e) => e.target.style.background = 'transparent'}
                                        >
                                            {d}
                                        </div>
                                    ))}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </motion.div>

                    {/* Driver 2 Selector */}
                    <motion.div
                        style={{
                            padding: 'var(--spacing-md)',
                            position: 'relative',
                            background: 'linear-gradient(145deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)',
                            backdropFilter: 'blur(16px)',
                            border: '1px solid var(--border-glass)',
                            borderRadius: 'var(--radius-lg)'
                        }}
                        initial={{ opacity: 0, x: 30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        <label style={{ color: 'var(--accent-gold)', fontWeight: 600, marginBottom: '8px', display: 'block' }}>
                            Driver 2
                        </label>
                        <input
                            type="text"
                            value={driver2 || search2}
                            onChange={(e) => {
                                setSearch2(e.target.value)
                                setDriver2('')
                                setShowDropdown2(true)
                            }}
                            onFocus={() => setShowDropdown2(true)}
                            onBlur={() => setTimeout(() => setShowDropdown2(false), 200)}
                            placeholder="Search driver..."
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
                        <AnimatePresence>
                            {showDropdown2 && filteredDrivers2.length > 0 && (
                                <motion.div
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    style={{
                                        position: 'absolute',
                                        top: '100%',
                                        left: 0,
                                        right: 0,
                                        background: 'var(--bg-secondary)',
                                        border: '1px solid var(--border-glass)',
                                        borderRadius: 'var(--radius-md)',
                                        maxHeight: '300px',
                                        overflowY: 'auto',
                                        zIndex: 1000,
                                        boxShadow: '0 10px 40px rgba(0,0,0,0.5)'
                                    }}
                                >
                                    {filteredDrivers2.map(d => (
                                        <div
                                            key={d}
                                            onMouseDown={(e) => {
                                                e.preventDefault()
                                                setDriver2(d)
                                                setSearch2('')
                                                setShowDropdown2(false)
                                            }}
                                            style={{
                                                padding: '10px 16px',
                                                cursor: 'pointer',
                                                borderBottom: '1px solid var(--border-glass)',
                                                transition: 'background 0.2s'
                                            }}
                                            onMouseEnter={(e) => e.target.style.background = 'var(--bg-glass-hover)'}
                                            onMouseLeave={(e) => e.target.style.background = 'transparent'}
                                        >
                                            {d}
                                        </div>
                                    ))}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </motion.div>
                </div>

                {/* Comparison Display */}
                {driver1 && driver2 && (
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        {/* Dynamic Chart.js Line Chart */}
                        <div className="glass-card" style={{
                            padding: 'var(--spacing-lg)',
                            marginBottom: 'var(--spacing-xl)',
                            position: 'relative'
                        }}>
                            <h3 style={{ marginBottom: 'var(--spacing-md)', textAlign: 'center' }}>
                                ELO History Comparison
                            </h3>
                            <div style={{ height: '400px', position: 'relative' }}>
                                {chartData ? (
                                    <Line data={chartData} options={chartOptions} />
                                ) : (
                                    <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                                        No ELO history data available for these drivers
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* Stats Comparison Table */}
                        <div className="glass-card" style={{ padding: 'var(--spacing-lg)' }}>
                            <h3 style={{ marginBottom: 'var(--spacing-md)', textAlign: 'center' }}>
                                Career Statistics
                            </h3>
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr>
                                        <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid var(--border-glass)' }}>Stat</th>
                                        <th style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', color: 'var(--accent-blue)' }}>{driver1}</th>
                                        <th style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', color: 'var(--accent-gold)' }}>{driver2}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style={{ padding: '12px', borderBottom: '1px solid var(--border-glass)' }}>Peak ELO</td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', fontWeight: 700, color: stats1?.peak_elo >= stats2?.peak_elo ? 'var(--accent-green)' : 'inherit' }}>
                                            {stats1?.peak_elo || 'N/A'}
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', fontWeight: 700, color: stats2?.peak_elo >= stats1?.peak_elo ? 'var(--accent-green)' : 'inherit' }}>
                                            {stats2?.peak_elo || 'N/A'}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '12px', borderBottom: '1px solid var(--border-glass)' }}>Avg ELO</td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', color: stats1?.avg_elo >= stats2?.avg_elo ? 'var(--accent-green)' : 'inherit' }}>
                                            {stats1?.avg_elo || 'N/A'}
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', color: stats2?.avg_elo >= stats1?.avg_elo ? 'var(--accent-green)' : 'inherit' }}>
                                            {stats2?.avg_elo || 'N/A'}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '12px', borderBottom: '1px solid var(--border-glass)' }}>Wins</td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', color: stats1?.wins >= stats2?.wins ? 'var(--accent-green)' : 'inherit' }}>
                                            {stats1?.wins || 0}
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)', color: stats2?.wins >= stats1?.wins ? 'var(--accent-green)' : 'inherit' }}>
                                            {stats2?.wins || 0}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '12px', borderBottom: '1px solid var(--border-glass)' }}>Total Races</td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)' }}>
                                            {stats1?.total_races || 0}
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid var(--border-glass)' }}>
                                            {stats2?.total_races || 0}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style={{ padding: '12px' }}>Win Rate</td>
                                        <td style={{ padding: '12px', textAlign: 'center' }}>
                                            {stats1 ? ((stats1.wins / stats1.total_races) * 100).toFixed(1) : 0}%
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center' }}>
                                            {stats2 ? ((stats2.wins / stats2.total_races) * 100).toFixed(1) : 0}%
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </motion.div>
                )}

                {/* Prompt to select drivers */}
                {(!driver1 || !driver2) && (
                    <motion.div
                        className="glass-card"
                        style={{
                            padding: 'var(--spacing-xl)',
                            textAlign: 'center',
                            color: 'var(--text-secondary)',
                            position: 'relative',
                            zIndex: 1
                        }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                    >
                        <p style={{ fontSize: '1.2rem' }}>
                            Select two drivers above to compare their career statistics and ELO history
                        </p>
                    </motion.div>
                )}
            </div>
        </main>
    )
}

export default Compare
