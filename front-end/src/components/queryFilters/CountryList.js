import React, { Component } from 'react';
import { connect } from 'react-redux';

import { setSelectedCountries } from "../../redux/actions/countries";

const countriesList = ["US", "Germany", "UK", "France"];

class CountryList extends Component {
    constructor(props) {
        super(props);

        this.state = { selectedCountries: [] };
    }

    render() {
        return (
            countriesList.map( (country, index) => ( <div key={index}>{country}</div> ) )
        );
    }
}

const mapStateToProps = store => ({
    // data: store.data
})

const mapDispatchToProps = dispatch => ({
    fetchData: (query) => dispatch(setSelectedCountries( this.state.selectedCountries ))
})

export default connect(mapStateToProps, mapDispatchToProps)(CountryList);