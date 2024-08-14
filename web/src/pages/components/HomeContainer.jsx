import React, { useState, useEffect } from 'react';
import './HomeContainer.css'
import Checkbox from '@mui/material/Checkbox';
import { styled } from '@mui/material/styles';


const HomeContainer = ({message_info}) => {

    return <section class="message-container">
        <img class="channel-img" src={`http://localhost:8080/api/get_channel_image/${message_info.channel.id}`} alt="" />
        <span class="text-primary">{message_info.content}</span>
    </section>
}

export default HomeContainer;