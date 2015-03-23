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
		return $('<div/>', { "class": "col-md-"+ options.fields.autocomplete.len})
				.append(StockAutocomplete(options.autoComplete, index));
	};

	var priceFieldFactory = function(index){
		return $('<div/>', { "class": "form-group col-md-"+ options.fields.price.len})
			.append(
				($('<input/>', {
					type: "text",
					name: options.fields.price["name"] + index,
					placeholder: "harga satuan",
					"class": "form-control"
				}))
			);
	};

	var amountFieldFactory = function(index){
		return $('<div/>', { "class": "form-group col-md-" + options.fields.amount.len})
			.append(
				$('<div/>', { "class": "input-group"})
					.append($('<input/>', {
						type: "text",
						name: options.fields.amount["name"] + index,
						placeholder: "jumlah",
						"class": "form-control"
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

	function getInputDiv(index) {
		var rowField = $('<div/>', {
			"class": "single-field form-inline",
		});

		if(options.fields.autocomplete)
			rowField.append(autocompleteFactory(index));

		if(options.fields.amount)
			rowField.append(amountFieldFactory(index));

		if(options.fields.price)
			rowField.append(priceFieldFactory(index));
		
		return rowField;
	}

	/**
	 * Add remove field functions
	 */
	function updateCounter(count){
		stockCounter.val(count);
	}

	getInputDiv(1).fadeIn('slow').appendTo(container);
	var i = container.find('.single-field').size();
	updateCounter(i);
	

	$(options.addButton).click(function(){
		i++;
		$(getInputDiv(i)).fadeIn('slow').appendTo(container);
		updateCounter(i);
	});

	$(options.removeButton).click(function(){
		if(i > 1){
			container.find('.single-field:last').remove();
			i--;
			updateCounter(i);
		}
	});
}