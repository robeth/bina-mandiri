var StockInput = function(container, options){
	
	/**
	 * Stock counter (number of row)
	 */
	var stockCounter = $('<input/>', {
		type: "hidden",
		id: options.counterName,
		name: options.counterName
	});


	var autocompleteFactory = function(index){
		var stockAutocomplete = new StockAutocomplete(options.autoComplete, index);
		var result = { 
			'html': $('<div/>', { "class": "col-md-"+ options.fields.autocomplete.len})
				.append(stockAutocomplete.html()),
			'stockAutocomplete' : stockAutocomplete
		}; 
		return result; 
	};

	var priceFieldFactory = function(index, initialPrice){
		initialPrice = typeof initialPrice !== 'undefined' ? initialPrice : "";
		return $('<div/>', { "class": "form-group col-md-"+ options.fields.price.len})
			.append(
				($('<input/>', {
					type: "text",
					name: options.fields.price["name"] + index,
					placeholder: "harga satuan",
					"class": "form-control",
					value: initialPrice
				}))
			);
	};

	var amountFieldFactory = function(index, initialAmount){
		initialAmount = typeof initialAmount !== 'undefined' ? initialAmount : "";
		return $('<div/>', { "class": "form-group col-md-" + options.fields.amount.len})
			.append(
				$('<div/>', { "class": "input-group"})
					.append($('<input/>', {
						type: "text",
						name: options.fields.amount["name"] + index,
						placeholder: "jumlah",
						"class": "form-control",
						value: initialAmount
					}))
					.append($('<div/>', {
						"class": "input-group-addon",
						text: "-"
					}))
			);
	};

	container.append(stockCounter);

	options.autoComplete.onStockUpdate = function(autoCompleteUi, newStock){
		var singleFieldContainer = autoCompleteUi.closest("div.single-field")
		if(options.fields.price)
			singleFieldContainer.find("input[name*='"+options.fields.price["name"]+"']").attr("placeholder", "stabil: " + newStock.stabil);
		
		if(options.fields.amount)
			singleFieldContainer.find("input[name*='"+options.fields.amount["name"]+"']").next().text(newStock.satuan);
	};

	function getInputDiv(index, data) {
		var rowField = $('<div/>', {
			"class": "single-field form-inline",
		});

		if(options.fields.autocomplete){
			stockAutocompleteInstance = autocompleteFactory(index); 
			rowField.append(stockAutocompleteInstance.html);
		}

		if(options.fields.amount)
			rowField.append(amountFieldFactory(index, data['jumlah']));

		if(options.fields.price)
			rowField.append(priceFieldFactory(index, data['harga']));
		
		// Init autocomplete field after all other components are loaded
		if(data){
			stockAutocompleteInstance.stockAutocomplete.forceUpdate(data);
		}

		return rowField;
	}

	var i = 0;

	/**
	 * Add remove field functions
	 */
	function updateCounter(count){
		stockCounter.val(count);
	}

	function addNewRow(data){
		i++;
		$(getInputDiv(i, data)).fadeIn('slow').appendTo(container);
		updateCounter(i);
	}

	function removeLastRow(initialData){
		if(i > 1){
			container.find('.single-field:last').remove();
			i--;
			updateCounter(i);
		}
	}

	$(options.addButton).click(addNewRow);

	$(options.removeButton).click(removeLastRow);

	if(options.initial){
		for(var j = 0; j < options.initial.length; j++){
			addNewRow(options.initial[j]);
		}
	} else {
		addNewRow();
	}

}