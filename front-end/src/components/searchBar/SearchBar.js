import React, { Component } from 'react';
import { connect } from 'react-redux';

import { fetchData } from "../../redux/actions/data";

import "./searchBar.css";

class SearchBar extends Component {
    constructor(props) {
        super(props);

        this.state = { query: "" }
    }

    componentDidMount() {
        this.searchButton.addEventListener("click", () => this.props.fetchData({ userQuery: this.input.value }) );
    }

    render() {
        return (
            <div className="search-bar search-bar">
                <input className="input-text" type="text" placeholder="Write something" ref={ el => this.input = el }/>
                <div><i className="fa fa-microphone icon" aria-hidden="true" ></i></div>
                <div><i className="fa fa-search icon" aria-hidden="true" ref={ el => this.searchButton = el }></i></div>
            </div>
        );
    }
}

const mapStateToProps = store => ({
    // data: store.data
})

const mapDispatchToProps = dispatch => ({
    fetchData: (query) => dispatch(fetchData(query))
})

export default connect(mapStateToProps, mapDispatchToProps)(SearchBar);