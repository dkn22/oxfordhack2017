import React, { Component } from 'react';
import { connect } from 'react-redux';

// import { fetchData } from "../../redux/actions/data";

import Logo from "../logo/Logo";
import SearchBar from "../searchBar/SearchBar";
// import QueryFilters from "../queryFilters/QueryFilters";
import ResultList from "../resultList/ResultList";

import "./home.css"

class Home extends Component {
    
    componentWillMount = () => {
        // this.props.fetchData({userQuery: "userQuery", dateFrom: "dateFrom", dateTo: "dateTo", country: "country", sources: "sources"});
    }

    render () {
        return (
            <div className="root-container">
                <Logo />
                <SearchBar />
                {/* <QueryFilters /> */}
                <ResultList />
            </div>
        );
    }
}

const mapStateToProps = store => ({
    // data: store.data
})

const mapDispatchToProps = dispatch => ({
    // fetchData: (query) => dispatch(fetchData(query))
})

export default connect(mapStateToProps, mapDispatchToProps)(Home);