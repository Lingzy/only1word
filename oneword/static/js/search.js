$(document).ready(function(){
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
                  article = result.data;
                  for (var i=0, len=article.length; i<len;i++){
                    $("#"+article[i].id).parent('.card').show();
                  }
                }
                else {
                  titlesearch=1;
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
})
