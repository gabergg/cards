function update(div) {
    if (div == 'all') {
        update('hand');
        update('board');
        return;
    }
    $('#' + div).load('http://' + location.hostname + ':' + location.port + location.pathname + '/' + div);
}

var ws;

$(document).ready(function() {
    console.log(myId);
    ws = new WebSocket('ws://' + location.hostname + ':' + location.port + '/' + myId + '/ws');
    //update('all');
    ws.onmessage = function(msg) {
        console.log(msg.data);
    }
});