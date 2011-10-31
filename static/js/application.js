$(function() {
  msg_form_field_resize();
  $(window).resize(msg_form_field_resize);
  
  $(".nav_bar").each(function(i) {
    var a = $(this).find("a");
    
    if (a.length > 0) {
      $(this).css("cursor","pointer");
      $(this).click(function() {
        window.location = a.attr("href");
      })
    }
  })
})

function msg_form_field_resize() {
  var field_width = $("#whole_page").width() - 80;
	$('.msg_form_field').css('width', field_width + 'px');
}