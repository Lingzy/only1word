$(document).ready(function(){
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

})
