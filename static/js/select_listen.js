// 获取 <select> 元素
var selectElement = document.getElementById("bgm");

// 添加 change 事件监听器
selectElement.addEventListener("change", function() {
  // 获取选择的选项值
  var selectedValue = this.value;
  
  // 执行相应的动作
  console.log("选择的选项值:", selectedValue);
  // 在这里执行你想要的动作
  var bgmAudio = document.getElementById("bgmAudio");
  bgmAudio.src = "static/bgm/" + selectedValue + ".mp3";
  bgmAudio.play();
});
