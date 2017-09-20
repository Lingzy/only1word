$(document).ready(function(){
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

})
