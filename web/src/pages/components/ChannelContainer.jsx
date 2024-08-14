import React, { useState, useEffect } from 'react';
import './ChannelContainer.css'
import Checkbox from '@mui/material/Checkbox';
import { styled } from '@mui/material/styles';

const WhiteBorderCheckbox = styled(Checkbox)({
  '&.MuiCheckbox-root': {
    color: 'white',
  },
});

const ChannelContainer = ({channel_info}) => {
    const [isChecked, setIsChecked] = useState(channel_info.selected);
    const on_change = (event) => {
        
        setIsChecked(event.target.checked);
        fetch(`http://localhost:8080/api/set_channel_select/${channel_info.id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({selected: !isChecked}),
          });
    }
    return <section class="channel-container">
        <WhiteBorderCheckbox
            checked={isChecked}
            onChange={on_change}
            name="dataCheckbox"
            color="primary"
          />
        <img class="channel-img" src={`http://localhost:8080/api/get_channel_image/${channel_info.id}`} alt="" />
        <span class="text-primary">{channel_info.name}</span>
    </section>
}

export default ChannelContainer;