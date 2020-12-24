'use strict';

// Input Redirect source URL & Redirect URL.
const redirectSrcHost = 'hogehoge.com';
const redirectHost = 'www.hogehoge.com';

exports.handler = (event, context, callback) => {
    
    const originalRequest = event.Records[0].cf.request;   

    //Extact require param from "originalRequest".
    const originalHost = originalRequest.headers.host[0].value;
    const originalUri = originalRequest.uri;
    
    // response to User or Origin.
    if (originalHost == redirectSrcHost){

        //Generate HTTP redirect response.
        const redirectResponse = {
            status: '301',
            statusDescription: 'Redirect',
            headers: {
            'location': [{
                key: 'Location',
                value: 'https://' + redirectHost + originalUri,
            }],
            },
        };

        callback(null, redirectResponse);
    } else {
        callback(null, originalRequest)
    }
};

