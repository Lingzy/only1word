$(document).ready(function(){

  // 隐藏用户old_password错误信息
  $('.old_password_error').hide();
  /*
  // 用户详情页如果文章少于5个则隐藏上下页按钮
  // var my_articles = $(".my_article").length;
  // if (my_articles < 5){
  //   $('.myarticle_arrow').hide();
  // }
  */

  var my_favorites = $(".my_favorite").length;
  if (my_favorites < 5){
    $('.myfavorite_arrow').hide();
  }

  var my_comments = $(".my_comment").length;
  if(my_comments < 5){
    $('.mycomment_arrow').hide();
  }

  $('.special.card .image').dimmer({
    on:'hover'
  });

// 修改密码modal
  $('#changepwd_btn').click(function(){
    $('.changepwd.modal').modal('show');
  })

  $('#bbtn').click(function(){
    $('.changepwd.modal').modal('show');
  })

// 密码表单验证
  $('.ui.changepwd.form')
  .form({
    on:'blur',
    fields:{
      // old_password验证
      old_password:{
        indentifier : 'old_password',
        rules:[
          {
            type:'empty',
            prompt:'Please enter old pwasword'
          }
        ]
      },
      // new_password1验证
      new_password1:{
        indentifier: 'new_password1',
        rules:[
          {
            type:'empty',
            prompt:'Please enter new password'
          },
          {
            type:'minLength[8]',
            prompt:'Your new password must be at least 8 characters'
          }
        ]
      },
      // new_password2验证
      new_password2: {
        identifier  : 'new_password2',
        rules: [
          {
            type   : 'empty',
            prompt : 'Please confirm you new password'
          },
          {
            type   : 'match[new_password1]',
            prompt : 'Password doesn\'t match the confirmation '
          }
        ]
      },
    }
  });

  $('#confirm_change_btn').click(function(){
    var old_password = $('#old_password').val();
    var new_password1 = $('#new_password1').val();
    var new_password2 = $('#new_password2').val();
    $.ajax({
      url:'/api/changepwd/',
      type:'post',
      async:false,
      data:{'old_password':old_password,
            'new_password1':new_password1,
            'new_password2':new_password2},
      success:function(result){
        if (result.status == 200) {
          $('.changepwd_done.modal').modal('show');

          return false;
        }
        if (result.status == 10021) {
          $('.old_password_error').show();
          $('#confirm_change_btn').attr("disabled",true);
          // return false;
        }
      }
    });
  });

  $(":input").focus(function(){
    // $('.ui.message').hide();
    $('.old_password_error').hide();
    $('#confirm_change_btn').attr("disabled",false);
  });

  $('.myarticle').click(function(){
    var id = $(this).attr("myarticle_id");
    $('[myarticle_md_id='+ id +']').modal('show');
  });

  $('.myfavorite').click(function(){
    var id = $(this).attr("myfavorite_id");
    $('[myfavorite_md_id='+ id +']').modal('show');
  });

  $('.mycomment').click(function(){
    var id = $(this).attr("mycomment_id");
    $('[mycomment_md_id='+ id +']').modal('show');
  });


})
