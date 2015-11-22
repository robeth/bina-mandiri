var NasabahAutocomplete = function(uiElement, formElement, dictionary, initialData){
	var updateCallback = function(newData){
		$(formElement).val(newData['id']);
	}

	var substringMatcher = function(strs) {
	    return function findMatches(q, cb) {
	        var matches, substrRegex;

	        // an array that will be populated with substring matches
	        matches = [];
	        // regex used to determine if a string contains the substring `q`
	        substrRegex = new RegExp(q.term.toLowerCase(), 'i');

	        // iterate through the pool of strings and for any string that
	        // contains the substring `q`, add it to the `matches` array
	        $.each(strs, function(i, entry) {
	            if (substrRegex.test(entry.nama.toLowerCase())) {
	                // the typeahead jQuery plugin expects suggestions to a
	                // JavaScript object, refer to typeahead docs for more info
	                entry.value = entry.nama
	                matches.push(entry);
	            }
	        });

	        cb(matches);
	    };
	};

	if(initialData){
		$(formElement).val(initialData['id'])
		$(uiElement).val(initialData['nama']);
	}

	uiElement.autocomplete({
		source: substringMatcher(dictionary),
		minLength: 2,
		autoFocus: true,
		selectFirst: true,
		focus: function(event, ui){
			updateCallback(ui.item)
		},
		select: function(event, ui){
			updateCallback(ui.item)
		}
	});
}
