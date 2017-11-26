import React, { Component } from 'react';
import { Progress } from 'reactstrap';

import { withRouter } from 'react-router'

import "./card.css"

class Card extends Component {
    
    componentDidMount() {
        this.link.addEventListener("click", () => this.props.history.push(this.props.data.id) );
    }

    render() {
        const {data} = this.props;
        // console.log(data)
        return (
            <div className="card-root">
                <div className="leftSide">
                    <div className="title">{data.title}</div>
                    <div className="agency">{data.source}</div>
                    <div className="url">{data.url}</div>                    
                </div>
                <div className="rightSide">
                    <div>score</div>
                    
                    <Progress multi>
                        <Progress bar color="danger" value={data.slant*100} />
                    </Progress>

                    <div ref= {el => this.link = el } id={data.id}>Click here to quote check</div>

                </div>
            </div>
        );
    }
}

export default withRouter(Card);