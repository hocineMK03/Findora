import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import SearchServices from '../services/SearchServices';
import './InformationPage.css';

export const InformationPage = () => {
  const { id } = useParams(); 
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await SearchServices.handleSearchSpecific({ document: id });

        if (result.status === 200) {
          setData(result.data);
        } else {
          console.log('Error fetching data:', result);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    console.log('herere');
  }, [id]);

  if (!data) return <div className="loading-text">Loading...</div>;

  return (
    <div className="information-container">
      <h1>Content Of  {id}</h1>
      <p>{data}</p>
    </div>
  );
};
