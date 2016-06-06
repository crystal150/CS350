/*
$(function() {
	$('#calculate').bind('click', function() {
		$.getJSON('http://localhost:5000/calculate', {
			text: $('#insult-input').val()
			}, function(data) {
				console.log(data);
				$("insult-input").css({'background-color' : '#FFFFEE'});
				//        $("#result").text(data);
			});
		return false;
	});
});
*/

$(function() {
	var textarea = $("#insult-input");
	var resultMessage = $("#result");
	textarea.bind('input propertychange', function() {
		/*
		var data = Math.random() * 100;
		data = data.toFixed(2);
		console.log(data);
		*/
		$.getJSON('http://localhost:5000/calculate', {
			text: textarea.val()
			}, function(data) {
				if (data > 50) {
				textarea.css("border-color", "#F19113");
				resultMessage.text("Possibility of insult is " + data + "%").css("color", "#F19113");
			}
			else {
				textarea.css("border-color", "#5CB85C");
				resultMessage.text("Possibility of insult is " + data + "%").css("color", "#5CB85C");
			}
		});
	return false;
	});
});

