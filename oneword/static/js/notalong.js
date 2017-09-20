$(document).ready(function(){
  $(".title_error").hide();
  $("#create_button").attr("disabled",false);

  // 点击文章显示文章与评论区modal
  $('.article').click(function(){
    var id = $(this).attr("id");
    var username = $("#login_user").text().replace(/[ \r\n]/g,"");
      $.ajax({url:"/api/myownarticle/",
              data:{"id":id,
                    "username":username},
              async:false,
              success:function(result){
                if (result.status == 200) {
                  alert("Sorry,you CAN NOT comment on your own articles");
                  // return false;
                }
                else {
                  $('[article_id='+ id +']').modal('show');
                }
              }
            });
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
        location.reload();
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

});
