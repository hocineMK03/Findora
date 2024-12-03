
import './App.css'
import { BrowserRouter as Router, Routes , Route } from 'react-router-dom'


import { HomePage } from './pages/HomePage'
import { ResultPage } from './pages/ResultPage'
import { InformationPage } from './pages/InformationPage'
import { NavBar } from './components/NavBar/NavBar'
import { Footer } from './components/Footer/Footer'
function App() {
  return (
   
    
     <Router>
     <NavBar />
      <Routes>
        
        <Route path="/" element={<HomePage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/information/:id" element={<InformationPage />} />
        <Route path="*" element={<div>Not Found</div>} />
      </Routes>

      <Footer />
     </Router>
    
  )
}

export default App
