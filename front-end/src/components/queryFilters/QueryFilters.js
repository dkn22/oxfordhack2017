import React, { Component } from 'react';

import Filter from "./Filter";
import SourceList from "./SourceList";
import CountryList from "./CountryList";
import DateSelector from "./DateSelector";

import "./queryFilters.css"

import newsSources from './newsSources.json';
import countries from './countries.json';

export default class QueryFilters extends Component {
    render() {
        return (
            <div className="query-filters">
                <div className="filters-container">
                    <Filter name="Any source" ><SourceList /></Filter>
                    <Filter name="Any country" ><CountryList /></Filter>
                    <Filter name="Any date" ><DateSelector /></Filter>
                </div>
            </div>
        );
    }
}