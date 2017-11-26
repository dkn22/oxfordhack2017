import { combineReducers } from "redux";

import initialState from "./initialState";
import { prefixes } from "../actions/_constants"

import getAsyncActionReducers from "./asyncActionReducer";

const dataReducers = getAsyncActionReducers({ 
    actionTypePrefix: prefixes.DATA,
    objectsInitialState: initialState.data,
    isFetchingInitialState: initialState.isFetchingData
});

export default combineReducers({
    data: dataReducers.objectsReducer,
    
    isFetchingData: dataReducers.isFetchingReducer,
});