import React from 'react';
import { Route, Switch, Link } from "wouter";
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import FormatListBulleted from '@mui/icons-material/FormatListBulleted';
import Channels from './pages/ChannelsPage';
import Messages from './pages/HomePage';

import "./App.css";

// Example components

const Home = () => <h2>home</h2>;

function App() {
  return (
    <section class="main-grid">
      <section class="menu-wrapper">
        <div class="card">
          <img src="/logo.webp" alt="" class="menu-logo"/>
        <nav className="menu">
          <ul>
            <li><Link href="/" style={{textDecoration: 'none'}}>
            <span class="menu-link"><HomeIcon className='menu-icon' /> Home</span>
            </Link></li>
            <li><Link href="/channels" style={{textDecoration: 'none'}}>
            <span class="menu-link" ><FormatListBulleted className='menu-icon' /> Channels</span></Link></li>
          </ul>
        </nav>
        </div>
      </section>
      <main class="card">
        <Switch>
          <Route path="/" component={Messages} />
          <Route path="/channels" component={Channels} />
        </Switch>
      </main>
    </section>
  );
}

export default App;