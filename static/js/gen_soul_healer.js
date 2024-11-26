var socket = io();
socket.on('connect', function () {
    console.log('Connected to Soul Healer server');
});

socket.on('soul_healer_result', function (data) {
    console.log("创建心理治愈师完成", data)
});