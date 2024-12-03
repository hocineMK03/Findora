

import { useState,useEffect} from 'react'
import './HomePage.css'

import searchSevices from '../services/SearchServices'
export const HomePage = () => {
   const [search, setSearch] = useState(
    {
      request:""
    }
   )  

  
  const handleSearch = async(e) => {
    e.preventDefault();
    const result=await searchSevices.handleSearch(search)
    
    if(result.status===200){
      
      const data=result.data
      sessionStorage.setItem("searchResults", JSON.stringify(data));

      
      window.location.href = '/result';
    }
    else{
      console.log('error')
    }
  }



  const handleChange = (e) => {
    

    
      const { name, value } = e.target;
      setSearch({ ...search, [name]: value });
    
  }

  useEffect(() => {

  })
  return (
    <div className='home-container'>
      <div className='home-content'>

        
        <div className='home-title'>
          
          <h1>Findora</h1>
          <p>Explore. Discover. Findora.</p>

        </div>
        

        <div className='home-search'>
        <textarea
    name="request"
    value={search.request}
    placeholder="Search for anything..."
    onChange={handleChange}
    rows="1" 
    className="dynamic-textarea"
  />          <button onClick={handleSearch}>Search</button>
        </div>

      </div>
    </div>
  )
}
