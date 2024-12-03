
import axios from "axios"
class SearchServices {

    constructor() {
        this.url=import.meta.env.VITE_API_URL

        
        }

        async handlePostRequests(data,endpoint){
            try{
            
                const body=data || {}
                const headers={
                    'Content-Type':'application/json'
                }
                let response=null
               
        
               
                 response= await axios({
                  method:"POST",
                  url:`${this.url}/${endpoint}`,
                  headers:headers,
                  data:JSON.stringify(body),
                  /* withCredentials:true */
              })
               
                
             
                
                return {
                    status: response.status,
                    data: response.data
                  };
        
            }   
            catch(error){
              
                return{
                    status: error.response.status,
                    data: error.response.data
                  };
                
            }
          }

    async handleSearch(data){
        return await this.handlePostRequests(data,"search")

    }

    async handleSearchSpecific(data){
        return await this.handlePostRequests(data,"searchspecific")

    }
}


export default new SearchServices()