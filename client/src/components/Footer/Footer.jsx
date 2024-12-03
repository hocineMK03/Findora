
import logo from '../../assets/logo3.png'
import './Footer.css'
export const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="footer-logo">
        <div
          className="navbar-logo1"
          
        >
          <img src={logo} alt="Logo" className="logo" />
          
        </div>
      </div>

      <div className="footer-text">
        <p>© {new Date().getFullYear()} Findora. All rights reserved.</p>
        
      </div>
    </footer>



  )
}
