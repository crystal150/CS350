  $(function() {
    $('#calculate').bind('click', function() {
      $.getJSON('http://localhost:5000/calculate', {
        text: $('#insult-input').val()
      }, function(data) {
				console.log(data);
        $("#result").text(data);
      });
      return false;
    });
  });
