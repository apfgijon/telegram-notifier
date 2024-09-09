import React from 'react';
import { Route, Switch, Link } from "wouter";
import HomeIcon from '@mui/icons-material/Home';
import FormatListBulleted from '@mui/icons-material/FormatListBulleted';
import Channels from './pages/ChannelsPage';
import Messages from './pages/HomePage';

import "./App.css";

// Example components

function App() {
  return (
    <section className="main-grid">
      <section className="menu-wrapper">
        <div className="card">
          <img src="/logo.webp" alt="" className="menu-logo"/>
        <nav className="menu">
          <ul>
            <li><Link href="/" style={{textDecoration: 'none'}}>
            <span className="menu-link"><HomeIcon className='menu-icon' /> Home</span>
            </Link></li>
            <li><Link href="/channels" style={{textDecoration: 'none'}}>
            <span className="menu-link" ><FormatListBulleted className='menu-icon' /> Channels</span></Link></li>
          </ul>
        </nav>
        </div>
      </section>
      <main className="card">
        <Switch>
          <Route path="/" component={Messages} />
          <Route path="/channels" component={Channels} />
        </Switch>
      </main>
    </section>
  );
}

export default App;