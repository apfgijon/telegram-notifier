import React, { useState, useEffect } from 'react';
import { ClipLoader } from 'react-spinners';
import "./HomePage.css"
import HomeContainer from './components/HomeContainer'

const Messages = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/get_messages');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      setData(result);
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <ClipLoader color="#36D7B7" loading={loading} size={50} />
      </div>);
  }

  if (error) {
    return <div>Error!</div>;
  }
  return (
    <section class="ChannelPage">
        <h1 class="text-primary">News</h1>
        <section class="ChannelPage-content">
          {data.map(news => <article key={news.id}><HomeContainer message_info={news}></HomeContainer></article>)}
        </section>
    </section>
  );
};

export default Messages;