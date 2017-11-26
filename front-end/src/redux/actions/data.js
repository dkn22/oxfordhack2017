import { prefixes, actionTypes } from "./_constants"
import getAsyncAction from "./asyncActionUtils"
import apis from "../../api/data"

export const fetchData = getAsyncAction({ actionTypePrefix: prefixes.DATA+actionTypes.FETCH, asyncFunc: apis.getData });