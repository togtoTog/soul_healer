var socket = io();
socket.on('connect', function () {
    console.log('Connected to server');
});

socket.on('scene_character_generated', function (data) {
    // 检测设备类型或屏幕尺寸
    var block = document.getElementById('loader-block');
    block.style.display = "none";
    // 在PC端加载PC端的JavaScript文件
    var block = document.getElementById('scene-character-block');

    var scene = data.scene;
    var scene_block = document.getElementById('scene');
    scene_block.value = scene;

    var character_1 = data.character_1;
    var character_1_block = document.getElementById('character_1');
    character_1_block.value = character_1;

    var character_2 = data.character_2;
    var character_2_block = document.getElementById('character_2');
    character_2_block.value = character_2;

    block.style.display = "flex";

});