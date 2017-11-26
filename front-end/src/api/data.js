import jsonData from './data.json';

// export default {
//     getData: ({userQuery, dateFrom="", dateTo="", country="", sources=""}) =>
//         fetch(`/todo/api/scores/?keyword=${userQuery}&datefrom=${dateFrom}&date=${dateTo}&sources=${sources}&country=${country}`)
//         .then( response => {
//             if (response.status !== 200) {
//                 console.error('Looks like there was a problem. Status Code: ' +response.status);
//                 return;
//             }           
  
//             response
//                 .json()
//                 .then(data => {
//                     console.log(jsonData.data)
//                     return jsonData.data;
//                 })
//                 .catch(error => {
//                     console.error('Fetch Error', error);
//                 });
//         })
//         .catch(error => {
//             console.error('Fetch Error', error);
//         })
// }

export default {
    getData: (userQuery) => new Promise( (resolve, reject) => resolve( jsonData ) )        
}