


import './ResultPage.css';


import { useEffect,useState } from 'react'
import searchSevices from '../services/SearchServices'
export const ResultPage = () => {
  const [search, setSearch] = useState(
    {
      request:""
    }
   )  

   const [length,setLength]=useState(0)
   const [searchRequest,setSearchRequest]=useState("")
  const handleSearch = async(e) => {
    e.preventDefault();
    try{
      const result=await searchSevices.handleSearch(search)
    
    if(result.status===200){
      
      const data=result.data
      sessionStorage.setItem("searchResults", JSON.stringify(data));
      sessionStorage.setItem("resultLength",data.length)
      sessionStorage.setItem("searchRequest",search.request)


      setLength(data.length)
      setSearchRequest(search.request)
      setData(data)
      
    }
    else{
      console.log('error')
    }
    }
    catch(e){
      console.log(e)
    }
  }



  const handleChange = (e) => {
    

    
      const { name, value } = e.target;
      setSearch({ ...search, [name]: value });
    
  }
  const [data, setData] = useState([]);
  
  const handleSearchSpecific = (id) => {
 
    window.location.href = `/information/${id}`;
  };
    
  useEffect(() => {
    const result = sessionStorage.getItem('searchResults');
    if (result) {
      setData(JSON.parse(result)); // Update the state with parsed data
      
    }

    const resultLength = sessionStorage.getItem('resultLength');
    if (resultLength) {
      setLength(resultLength); 
      
    }

    const searchRequest = sessionStorage.getItem('searchRequest');
    if (searchRequest) {
      setSearch({ ...search, ["request"]: searchRequest })
      
    }
  }, []);
  return (
    <div className="result-container">
      <div className='home-search'>
        <textarea
    name="request"
    value={search.request }
    placeholder="Search for anything..."
    onChange={handleChange}
    rows="1" 
    className="dynamic-textarea"
  />          <button onClick={handleSearch}>Search</button>
        </div>
    {data.length > 0 ? (
      <ul>
        <div className='result-length'>
        <p>there is {length} documents</p>
        </div>
        {data.map((item, index) => (
          <li key={index} onClick={()=>{
            handleSearchSpecific(item.doc_id)
          }}>
            <strong>{item.doc_id}</strong>
            <p>{item.snippet}...</p>
            <span>Score: {item.score}</span>
          </li>
        ))}
      </ul>
    ) : (
      <p>No results found</p>
    )}
  </div>
  )
}
