$(document).ready(function(){
  $(".title_error").hide();
  $("#create_button").attr("disabled",false);

  // 点击文章显示文章与评论区modal
  $('.article').click(function(){
    var id = $(this).attr("id");
    $('[article_id='+ id +']').modal('show');

  });

 // 创建文章modal显示
  $('#create').click(function(){
    $('#create_new').modal('show');
  });

  // 判断文章title是否重复
  $('#article_title').blur(function(){
    var title = $(this).val();
    $.get("/api/title_search/",{"title":title},function(result){
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

  // 添加收藏文章
  $(".favorite").toggle(

    function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.ajax({
      url:"/api/favorite/",
      data:{"extra_id":id},
      async:false,
      success:function(result){
      if (result.status == 200) {
        $('[extra_id='+ result.article_id +']').find('a.favorite').html("<i class='heart icon'></i>"+result.favorite);
        return false;
      }
      else if (result.status === 10022 ) {
        alert("Eh,You DO NOT need to collect your own articles");
        return false;
      }
      else if (result.status === 10024){
        alert("you have collected this article");
        return false;
      }
      if (result.status == 10020){
        location.href="accounts/login/";
      }
    }});
  },
  function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.ajax({
      url:"/api/unfavorite/",
      data:{"extra_id":id},
      async:false,
      success:function(result){
      if (result.status == 200) {
        $('[extra_id='+ result.article_id +']').find('a.favorite').html(
          "<i class='empty heart icon'></i>"+result.favorite);
        // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
      }
      else if (result.status === 10022 ) {
        alert("somthing wrong");
        return false;
      }
      if (result.status == 10020){
        location.href="accounts/login/";
      }
    }});
  }
);

  // 取消收藏文章
  // $(".unfavorite").bind("click",function(){
  //   var id = $(this).parent('.extra.content').attr('extra_id');
  //   $.get("/api/unfavorite/",{"extra_id":id},function(result){
  //     if (result.status == 200) {
  //       $('[extra_id='+ result.article_id +']').find('a.unfavorite').attr('class','favorite').html(
  //         "<i class='empty heart icon'></i>"+result.favorite);
  //       // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
  //     }
  //     else if (result.status === 10022 ) {
  //       alert("somthing wrong");
  //     }
  //     if (result.status == 10020){
  //       location.href="accounts/login/";
  //     }
  //   })
  // });

  $.goup({
      trigger: 100,
      bottomOffset: 50,
      locationOffset: 280,
      title: 'TOP',
      titleAsText: true
  });

});
