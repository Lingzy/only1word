$(document).ready(function(){
  $(".title_error").hide();
  $("#create_button").attr("disabled",false);

  // 点击文章显示文章与评论区modal
  $('.article ').click(function(){
    var x = $(this).attr("id");
    $('[article_id='+ x +']').modal('show');
  });

 // 创建文章modal显示
  $('#create').click(function(){
    $('#create_new').modal('show');
  });

  // 判断文章title是否重复
  $('#article_title').blur(function(){
    var title = $(this).val();
    $.post("/api/title_search/",{"title":title},function(result){
      if (result.status == 200){
        $(".title_error").show();
        $("#create_button").attr("disabled",true);
      }
      else{
        $(".title_error").hide();
        $("#create_button").attr("disabled",false);
      }
    })
  });

  // 聚焦用户名输入框时隐藏错误提示信息
  $("#id_username").focus(function(){
    $(".errorlist").hide();
  });

  // 创建文章form表单验证
  $('.ui.form')
  .form({
    on:'blur',
    fields:{
      // 标题为空验证
      title:{
        indentifier : 'title',
        rules:[
          {
            type:'empty',
            prompt:'Please enter a title'
          }
        ]
      },
      // tags为空验证
      tags:{
        indentifier: 'tags',
        rules:[
          {
            type:'empty',
            prompt:'Please enter tags'
          }
        ]
      },
      // 文章内容为空，长度限制验证
      newcontent: {
        identifier  : 'newcontent',
        rules: [
          {
            type   : 'minLength[15]',
            prompt : 'Please enter at least 15 characters'
          },
          {
            type   : 'maxLength[150]',
            prompt : 'Please enter at most 150 characters'
          }
        ]
      },
      // 评论为空，长度限制验证
      comment_content: {
        identifier  : 'comment_content',
        rules: [
          {
            type   : 'minLength[15]',
            prompt : 'Please enter at least 15 characters'
          },
          {
            type   : 'maxLength[60]',
            prompt : 'Please enter at most 150 characters'
          }
        ]
      },
    }
  });

  // 设置ajax同步请求


  // 搜索文章
  $('.prompt').change(function(){
    var strings = $(this).val().replace(/\ +/g,"");
    var titlesearch=0;
    var authorsearch=0;
    var tagsearch=0;
    if (strings){
      $('.card').hide();
      // 通过标题搜索
      $.ajax({url:"/api/title_search/",
              async:false,
              data:{"title":strings},
              success:function(result){
                if (result.status == 200){
                  // var id = result.data["id"];
                  article = result.data;
                  for (var i=0, len=article.length; i<len;i++){
                    $("#"+article[i].id).parent('.card').show();
                  }
                }
                else {
                  titlesearch=1;
                  // if (titlesearch === 1 && authorsearch === 1){
                  //   $('.empty.modal').modal('show');
                  // }
                }
              }});
      $.ajax({url:"/api/author_search/",
              async:false,
              data:{"author":strings},
              success:function(result){
                if (result.status == 200){
                  // var id = result.data["id"];
                  article = result.data;
                  for (var i=0, len=article.length; i<len;i++){
                    $("#"+article[i].id).parent('.card').show();
                  }
                }
                else {
                  authorsearch=1;
                  // if (titlesearch === 1 && authorsearch === 1){
                  //   $('.empty.modal').modal('show');
                  // }
                }
              }});

      // 通过tags搜索
      $.ajax({url:"/api/tag_search/",
              async:false,
              data:{"tags":strings},
              success:function(result){
                if (result.status == 200){
                  // var id = result.data["id"];
                  article = result.data;
                  for (var i=0, len=article.length; i<len;i++){
                    $("#"+article[i].id).parent('.card').show();
                  }
                }
                else {
                  tagsearch=1;
                  // if (titlesearch === 1 && authorsearch === 1){
                  //   $('.empty.modal').modal('show');
                  // }
                }
              }});

      if (titlesearch==1 && authorsearch==1 && tagsearch==1){
        $('.empty.modal').modal('show');
      }
    }

    else{
      $('.card').show();
      $('.nostring.modal').modal('show');
    }
  });

  // 添加喜欢文章
  $(".like").click(function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.ajax({url:"/api/like/",
            data:{"extra_id":id},
            async:false,
            success:function(result){
              if (result.status == 200) {
                $('[extra_id='+ result.article_id +']').find('a.like').attr('class','dislike').html(
                  "<i class='thumbs up icon'></i>"+result.like);
                // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
              }
              if (result.status == 10020){
                location.href="accounts/login/"
              }
            }});
  });

  // 取消喜欢文章
  $(".dislike").click(function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.ajax({url:"/api/dislike/",
            data:{"extra_id":id},
            async:false,
            success:function(result){
              if (result.status == 200) {
                $('[extra_id='+ result.article_id +']').find('a.dislike').attr('class','like').html(
                  "<i class='thumbs outline up icon'></i>"+result.like);
                // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
              }
            }});
  });

  // 添加收藏文章
  $(".favorite").click(function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.get("/api/favorite/",{"extra_id":id},function(result){
      if (result.status == 200) {
        $('[extra_id='+ result.article_id +']').find('a.favorite').attr('class','unfavorite').html(
          "<i class='heart icon'></i>"+result.favorite);
        // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
      }
      if (result.status == 10020){
        location.href="accounts/login/"
      }
    })
  });

  // 取消收藏文章
  $(".unfavorite").click(function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.get("/api/unfavorite/",{"extra_id":id},function(result){
      if (result.status == 200) {
        $('[extra_id='+ result.article_id +']').find('a.unfavorite').attr('class','favorite').html(
          "<i class='empty heart icon'></i>"+result.favorite);
        // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
      }
    })
  });

  // 用户详情页如果文章少于5个则隐藏上下页按钮
  var my_articles = $(".my_article").length;
  if (my_articles < 5){
    $('.myarticle_arrow').hide()
  }

  var my_favorites = $(".my_favorite").length;
  if (my_favorites < 5){
    $('.myfavorite_arrow').hide()
  }

  var my_likes = $(".my_like").length;
  if(my_likes < 5){
    $('.mylike_arrow').hide()
  }

});
