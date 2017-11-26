import React, { Component } from 'react';

import threeJsEntryPoint from "./js/main"

import "./logo.css"

export default class Logo extends Component {

    componentDidMount() {
        threeJsEntryPoint(this.root);
    }

    render() {
        return (
            <div className="logo-container" >
                <div className="logo-div" ref={element => this.root = element}></div>
            </div>
        );
    }
}