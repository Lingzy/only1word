$(document).ready(function(){
  // 聚焦用户名输入框时隐藏错误提示信息
  $("#id_username").focus(function(){
    $(".errorlist").hide();
  });

  // 修改密码
  $('.special.card .image').dimmer({
    on:'hover'
  });
})
