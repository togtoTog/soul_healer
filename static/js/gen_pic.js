var socket = io();
socket.on('connect', function () {
    console.log('Connected to server');
});

socket.on('image_generated', function (data) {
    var img = document.createElement('img');
    var block = document.getElementById('lines-block');
    var image_path = data.image_path;
    img.src = image_path;
    // 检测设备类型或屏幕尺寸
    if (window.innerWidth >= 768) {
        // 在PC端加载PC端的JavaScript文件
        img.style.width = '300px'; // 设置固定宽度
        img.style.height = '300px'; // 设置固定高度
        img.style.marginTop = '10px';
    } else {
        // 在移动端执行移动端的代码逻辑
        img.style.width = '250px'; // 设置固定宽度
        img.style.height = '250px'; // 设置固定高度
        img.style.marginTop = '10px';
    }
    img.classList.add('moving-image');
    const box = document.createElement('div');
    box.classList.add('image-box'); // 添加 class
    box.appendChild(img);
    const div = document.createElement('div');
    div.classList.add('block'); // 添加 class
    div.style.textAlign = "left"
    div.appendChild(box);
    const explanationText = data.answer;
    const p = document.createElement('p');
    p.textContent = explanationText;
    div.appendChild(p);
    document.body.insertBefore(div, block);
    var audio = document.getElementById("myAudio");
    audio.src = data.voice;
    audio.play();
});