// 监听图片生成  
function generateImage() {
  document.getElementById('loader-block').style.display = 'block';
  var theme = document.getElementById('myInput').value;
  var audio = document.getElementById("myAudio");
  var style = document.getElementById("style").value;
  console.log("台词风格：", style)
  var frame = document.getElementById("frame").value;
  console.log("画面风格：", frame)
  audio.play();
  audio.pause();
  socket.emit('generate_image', { theme: theme, style: style, frame: frame });
}

// 人机共创用
function generateSceneCharacter() {
  document.getElementById('loader-block').style.display = 'block';
  var theme = document.getElementById('myInput').value;
  var style = document.getElementById("style").value;
  console.log("台词风格：", style)
  var frame = document.getElementById("frame").value;
  console.log("画面风格：", frame)
  socket.emit('generate_scene_character', { theme: theme, style: style, frame: frame  });
}

// 心理治愈用
function createSoulHealer() {
  document.getElementById('loader-block').style.display = 'block';
  var theme = document.getElementById('myInput').value;
  var style = document.getElementById("style").value;
  var frame = document.getElementById("frame").value;
  socket.emit('create_soul_healer', {theme: theme, style: style, frame: frame});
}

// 平行宇宙用
function generateSceneCharacter2() {
  document.getElementById('loader-block').style.display = 'block';
  var theme = document.getElementById('myInput').value;
  var style = document.getElementById("style").value;
  console.log("台词风格：", style)
  var frame = document.getElementById("frame").value;
  console.log("画面风格：", frame)
  socket.emit('generate_scene_character2', { theme: theme, style: style, frame: frame  });
}

// 人机共创启动
function generateImageWithPeople() {
  document.getElementById('loader-block').style.display = 'block';
  // document.getElementById('scene-character-block').style.display = 'none';
  document.getElementById('lines').value = "";
  var theme = document.getElementById('myInput').value;
  var scene = document.getElementById('scene').value;
  var character_1 = document.getElementById('character_1').value;
  var character_2 = document.getElementById('character_2').value;
  var audio = document.getElementById("myAudio");
  var style = document.getElementById("style").value;
  console.log("台词风格：", style)
  var frame = document.getElementById("frame").value;
  console.log("画面风格：", frame)
  audio.play();
  audio.pause();
  socket.emit('generate_image_with_people', { theme: theme, scene: scene, character_1: character_1, character_2: character_2, style: style, frame: frame});
}

// 人机共创互动
function generateImageWithLines() {
  document.getElementById('loader-block').style.display = 'block';
  var lines_block = document.getElementById('lines-block');
  lines_block.style.display = "none";
  var lines = document.getElementById('lines').value;
  var audio = document.getElementById("myAudio");
  audio.play();
  audio.pause();
  socket.emit('generate_image_with_lines', { lines: lines });
}

// 平行宇宙启动
function generateImageMultiverse() {
  document.getElementById('loader-block').style.display = 'block';
  // document.getElementById('scene-character-block').style.display = 'none';
  document.getElementById('lines').value = "";
  var theme = document.getElementById('myInput').value;
  var scene = document.getElementById('2scene').value;
  var character_1 = document.getElementById('2character_1').value;
  var character_2 = document.getElementById('2character_2').value;
  var audio = document.getElementById("myAudio");
  var style = document.getElementById("style").value;
  console.log("台词风格：", style)
  var frame = document.getElementById("frame").value;
  console.log("画面风格：", frame)
  audio.play();
  audio.pause();
  socket.emit('generate_image_multiverse', { theme: theme, scene: scene, character_1: character_1, character_2: character_2, style: style, frame: frame });
}

// 平行宇宙互动
function generateImageMultiverse2() {
  document.getElementById('loader-block').style.display = 'block';
  document.getElementById('multiverse-block').style.display = 'none';
  // 获取选中的单选框元素
  var selectedRadioButton = document.querySelector('input[name="radio-group"]:checked');
  if (selectedRadioButton) {
    var selectedLabel = document.querySelector('label[for="' + selectedRadioButton.id + '"]');
    var selectedLabelContent = selectedLabel.textContent;
    var lines = selectedLabelContent;
    var audio = document.getElementById("myAudio");
    audio.play();
    audio.pause();
    socket.emit('generate_image_multiverse2', { lines: lines });
  } else {
    console.log('未选择任何选项');
  }
}
