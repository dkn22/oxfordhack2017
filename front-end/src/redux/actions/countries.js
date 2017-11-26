import { prefixes, actionTypes } from "./_constants"
import getAsyncAction from "./asyncActionUtils"

export const setSelectedCountries = getAsyncAction({ actionTypePrefix: prefixes.DATA+actionTypes.FETCH, asyncFunc: () => console.log("not implemented") });