import React, { Component } from 'react';

import Dialog from "../common/Dialog";

import "./filter.css"

export default class Filter extends Component {
    constructor(props) {
        super(props);

        this.state = { showDialog: false }
    }

    componentDidMount = () => {
        this.filterContainer.addEventListener("click", () => this.setState({ showDialog: !this.state.showDialog }));
    }

    render() {
        return (
            <div className="filter-container text-unselectable" ref={el => this.filterContainer = el}>
                <div className="text">{this.props.name}</div>
                <i className="fa fa-angle-down" aria-hidden="true"></i>

                { 
                    this.state.showDialog &&
                    <Dialog>{this.props.children}</Dialog>
                }    
            </div>
        );
    }
}