var socket = io();
socket.on('connect', function () {
    console.log('Connected to server');
});

socket.on('image_multiverse', function (data) {
    var block = document.getElementById('loader-block');
    block.style.display = "none";
    var option1Label = document.getElementById('option1-label');
    option1Label.textContent = data.answer_1
    var option2Label = document.getElementById('option2-label');
    option2Label.textContent = data.answer_2
    var option3Label = document.getElementById('option3-label');
    option3Label.textContent = data.answer_3
    var block = document.getElementById('multiverse-block');
    block.style.display = "flex";
});