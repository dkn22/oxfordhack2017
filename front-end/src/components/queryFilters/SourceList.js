import React, { Component } from 'react';

export default class SourceList extends Component {
    render() {
        const sources = this.props.sources.list;
        return (
            sources.map( (source, index) => ( <div key={index}>source</div> ) )
        );
    }
}