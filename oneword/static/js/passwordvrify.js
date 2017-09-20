$(document).ready(function(){
  $('#changepwd').click(function(){
    var username = $('.username').text()
    var old_password = $("[name='old_password']")
    var new_password1 = $("[name='new_password1']")
    var new_password2 = $("[name='new_password2']")
    $.ajax({
      type:'post',
      url:"/api/changepwd/",
      async:false,
      data:{'username':username,
            'old_password':old_password,
            'new_password1':new_password1,
            'new_password2':new_password2},
      success:function(result){
        if (result.status == ) {

        }
      }
    })
  })
})
