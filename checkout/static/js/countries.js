$(document).ready(function() {
	$.getJSON("/static/json/countries.json", function(data) {
		console.log("Countries data loaded:", data);
		$.each(data, function(index, item) {
			console.log("Adding country:", item.country);
			$('#country').append(
				'<option value="' + item.code + '">' + item.country + '</option>'
			);
		});
	}).fail(function() {
		console.log("Failed to load countries.json");
	});
});