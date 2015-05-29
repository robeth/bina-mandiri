var StockAutocomplete = function(options, index){
	var stockContainer = $('<div>/');

	var stockInput = $('<input/>', {
		type: "text",
		"class": "form-control"
	});

	var stockHidden = $('<input/>', {
		name: options.fieldName,
		type: "hidden",
		value: "-"
	});

	var additionalElement = null;

	if(options.additionalInfo){
		additionalElement = $(options.additionalInfo.htmlTag, {
			id: options.additionalInfo.key + "index"
		});
	}

	var updateCallback = function(newStock, isUpdateStok){
		stockHidden.val(newStock[options.key].toString());

		if(isUpdateStok){
			stockInput.val(newStock.nama)
		}
		if(additionalElement){
			options.additionalInfo.renderCallback(additionalElement, newStock[options.additionalInfo.key]);
		}
		if(options.onStockUpdate){
			options.onStockUpdate(stockContainer,newStock);
		}
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
	        $.each(strs, function(i, stockEntry) {
	            if (substrRegex.test(stockEntry.nama.toLowerCase()) || substrRegex.test(stockEntry.kode.toLowerCase())) {
	                // the typeahead jQuery plugin expects suggestions to a
	                // JavaScript object, refer to typeahead docs for more info
	                stockEntry.value = stockEntry.nama
	                matches.push(stockEntry);
	            }
	        });

	        cb(matches);
	    };
	};

	stockInput.autocomplete({
		source: substringMatcher(options.stockData),
		minLength: 0,
		autoFocus: true,
		selectFirst: true,
		focus: function(event, ui){
			updateCallback(ui.item)
		},
		select: function(event, ui){
			updateCallback(ui.item)
		}
	}).autocomplete("instance")._renderItem = function(ul, item){
		return $("<li>")
			.append("<code>" + item.kode + "</code>" + item.nama)
			.appendTo(ul);
	};

	stockContainer
		.append(stockHidden)
		.append(stockInput);

	if(additionalElement){
		stockContainer.append(additionalElement);
	}

	this.forceUpdate = function(stock){
		for(var i = 0; i < options.stockData.length; i++){
			if(options.stockData[i][options.key] == stock[options.key]){
				updateCallback(options.stockData[i], true);
			}
		}
	}

	this.html = function(){
		return stockContainer;
	}
}