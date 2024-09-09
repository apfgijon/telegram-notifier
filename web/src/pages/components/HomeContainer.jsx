import React, { useState, useEffect } from 'react';
import { CSSTransition } from 'react-transition-group';
import './HomeContainer.css';

function formatDate(date) {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    return `${day}-${month}-${year} ${hours}:${minutes}`;
}

const tags = {
    "ORIENTE_MEDIO": {
        tag: "Oriente medio",
        color: "rgb(152, 29, 29)",
    },
    "UCRANIA": {
        tag: "Ucrania",
        color: "rgb(31, 134, 31)",
    },
    "USA": {
        tag: "EE.UU",
        color: "rgb(187, 29, 187)",
    },
    "VENEZUELA": {
        tag: "Venezuela",
        color: "rgb(183, 183, 11)",
    },
    "OTRO": {
        tag: "Otro",
        color: "grey",
    },
}

const HomeContainer = ({ message_info }) => {
    const [showAdditional, setShowAdditional] = useState(false);

    const toggleAdditional = () => {
        setShowAdditional(!showAdditional);
    };

    const content = message_info.analysis.find(a => a.typ === "TRANSLATE")?.tag ?? message_info.content;
    let tag = message_info.analysis.find(a => a.typ === "TAG")?.tag ?? "";
    let tag_content = "";
    let tag_color = "";
    if (tag in tags) {
        tag_content = tags[tag]?.tag;
        tag_color = tags[tag]?.color;
    }
    const additonal_info = message_info.analysis.filter(a => a.typ !== "TRANSLATE" && a.typ !== "TAG");
    return <section>
        <article className="message-container">
            <span className="date-container">{formatDate(new Date(message_info.date))}</span>
            <span className="tag-container" style={{ '--bg-color': tag_color }}>{tag_content}</span>
            <span className="drop-down-icon" onClick={toggleAdditional}>
                {
                    showAdditional ?
                        "arrow_drop_up" :
                        "arrow_drop_down"
                }
            </span>
            <img className="channel-img" src={`http://localhost:8080/api/get_channel_image/${message_info.channel.id}`} alt="" />

            <span className="text-primary message-content">{content}</span>
        </article>

        <CSSTransition
            in={showAdditional}
            timeout={300}
            classNames="slide"
            unmountOnExit
        >
            <section className='additional-info'>
                {
                    additonal_info.map(element =>
                        <section>
                            <article className="additional-typ">
                                {element.typ}
                            </article>
                            <article className="additional-content">
                                {element.tag}
                            </article>
                        </section>
                    )
                }
            </section>

        </CSSTransition>


    </section>
}

export default HomeContainer;