import React, { useState, useEffect, useRef  } from 'react';
import { ClipLoader } from 'react-spinners';
import "./HomePage.css"
import HomeContainer from './components/HomeContainer'

const Messages = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('Connecting');
  const ws = useRef(null);

  useEffect(() => {
    
    fetchData();
    ws.current = new WebSocket('ws://localhost:8080/updates');

    ws.current.onopen = () => setStatus('Connected');
    ws.current.onclose = () => setStatus('Disconnected');
    ws.current.onerror = () => setStatus('Error');

    ws.current.onmessage = (event) => {
      setData((d) => [...d, JSON.parse(event.data)] )
    };

    return () => {
      ws.current.close();
    };
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
    <section className="ChannelPage">
        <h1 className="text-primary">News</h1>
        <section className="ChannelPage-content">
          {data.sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0,40).map(news => <article key={news.id}><HomeContainer message_info={news}></HomeContainer></article>)}
        </section>
    </section>
  );
};

export default Messages;