import React, { Component } from 'react';
import { connect } from 'react-redux';

import Card from "./Card";

import "./resultList.css"

class ResultList extends Component {
    render() {
        let {data} = this.props;
        
        if(data.get(0))
            data = data.get(0).data;
            
        return (
            <div className="cards-container">
                { data.map( (entry, indx) => <Card key={indx} className="result-list" data={entry} /> ) }
            </div>
        );
    }
}

const mapStateToProps = store => ({
    data: store.data
})

const mapDispatchToProps = dispatch => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(ResultList);