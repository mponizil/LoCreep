// this javascript file is for profile page only (adjusts the width of input text field)

$(document).ready(function(){
    var elem = $('#chat');
	var field_width = elem.width() - 70;
	$('.msg_form_field').attr('style', 'margin-left: 4px; width: '+ (field_width) + 'px;');		
});

$(function(){
  $(window).resize(function(){
    var elem = $('#chat');
	var field_width = elem.width() - 70;
	$('.msg_form_field').attr('style', 'margin-left: 4px; width: '+ field_width + 'px;');
  });
});
