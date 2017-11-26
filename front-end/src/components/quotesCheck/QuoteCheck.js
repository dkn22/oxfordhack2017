import React, { Component } from 'react';
import { withRouter } from 'react-router'
import { connect } from 'react-redux';

class QuoteCheck extends Component {
    render() {
        const articleId = this.props.location.pathname.substring(1);        
        const {data_store} = this.props;

        const data = data_store.find( element => element.id === articleId); 

        return (
            <div>
                { data && data.map( ( item, indx ) => <div key="indx">{item}</div> )  }
            </div>
        );
    }
}

const mapStateToProps = store => ({
    data_store: store.data
})

const mapDispatchToProps = dispatch => ({
    // fetchData: (query) => dispatch(fetchData(query))
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(QuoteCheck));