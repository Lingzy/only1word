$(document).ready(function(){
  $(".title_error").hide();
  $("#create_button").attr("disabled",false);

  $('.article ').click(function(){
    var x = $(this).attr("id");
    $('[article_id='+ x +']').modal('show');
  });


  $('#create').click(function(){
    $('#create_new').modal('show');
  });


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


  $("#id_username").focus(function(){
    $(".errorlist").hide();
  });


  $('.ui.form')
  .form({
    on:'blur',
    fields:{
      title:{
        indentifier : 'title',
        rules:[
          {
            type:'empty',
            prompt:'Please enter a title'
          }
        ]
      },
      tags:{
        indentifier: 'tags',
        rules:[
          {
            type:'empty',
            prompt:'Please enter tags'
          }
        ]
      },
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
      follow_content: {
        identifier  : 'follow_content',
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


  $('.menu .item')
    .tab()
  ;

// 搜索文章
  $('.prompt').change(function(){
    var strings = $(this).val().replace(/\ +/g,"");
    var titlesearch=0;
    var authorsearch=0;
    if (strings){
      $('.card').hide();
      $.get("/api/title_search/",{"title":strings},function(result){
        if (result.status == 200){
          // var id = result.data["id"];
          article = result.data;
          for (var i=0, len=article.length; i<len;i++){
            $("#"+article[i].id).parent('.card').show();
          }
        }
        else {
          titlesearch=1;
          if (titlesearch === 1 && authorsearch === 1){
            $('.empty.modal').modal('show');
          }
        }
      });
      $.get("/api/author_search/",{"author":strings},function(result){
        if (result.status == 200){
          // var id = result.data["id"];
          article = result.data;
          for (var i=0, len=article.length; i<len;i++){
            $("#"+article[i].id).parent('.card').show();
          }
        }
        else {
          authorsearch=1;
          if (titlesearch === 1 && authorsearch === 1){
            $('.empty.modal').modal('show');
          }
        }
      });
    }

    else{
      $('.card').show();
      $('.nostring.modal').modal('show');
    }
  });

  $(".like").click(function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.get("/api/like/",{"extra_id":id},function(result){
      if (result.status == 200) {
        $('[extra_id='+ result.article_id +']').find('a.like').html(
          "<i class='thumbs up icon'></i>"+result.like);
        // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
      }
      if (result.status == 10020){
        location.href="accounts/login/"
      }
    })
  });

  $(".favorite").click(function(){
    var id = $(this).parent('.extra.content').attr('extra_id');
    $.get("/api/favorite/",{"extra_id":id},function(result){
      if (result.status == 200) {
        $('[extra_id='+ result.article_id +']').find('a.favorite').html(
          "<i class='heart icon'></i>"+result.favorite);
        // $('[extra_id='+ result.id +']').find('i.up').attr("class","thumbs up icon");
      }
      if (result.status == 10020){
        location.href="accounts/login/"
      }
    })
  });

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
