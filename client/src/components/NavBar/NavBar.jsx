

import logo from '../../assets/logo2.png'


import './NavBar.css'
export const NavBar = () => {
 
  const hrefrepo="https://github.com/hocineMK03/Findora"
  return (
    <nav className='nav'>
      <div className='nav-container'>
      <div className='logo'>
        <img src={logo} alt='logo' onClick={()=>{
          window.location.href='/'
        }}/>
      </div>

      <ul className='nav-links'>

        <li>
          <a href='/'>Home</a>
        </li>
        
        <li>
          <a href={hrefrepo}>Our Repo</a>
        </li>
      </ul>
      </div>
      
      
    </nav>
  )
}
