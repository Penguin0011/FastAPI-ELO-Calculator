import { Link, useLocation } from 'react-router-dom'

function Navbar() {
    const location = useLocation()

    const isActive = (path) => location.pathname === path

    return (
        <nav className="navbar">
            <div className="container navbar-content">
                <Link to="/" className="navbar-logo">
                    F1 <span>ELO</span>
                </Link>
                <div className="navbar-links">
                    <Link
                        to="/"
                        className={`navbar-link ${isActive('/') ? 'active' : ''}`}
                    >
                        Home
                    </Link>
                    <Link
                        to="/all-time"
                        className={`navbar-link ${isActive('/all-time') ? 'active' : ''}`}
                    >
                        All-Time Peak
                    </Link>
                    <Link
                        to="/2025"
                        className={`navbar-link ${isActive('/2025') ? 'active' : ''}`}
                    >
                        2025 Grid
                    </Link>
                </div>
            </div>
        </nav>
    )
}

export default Navbar
