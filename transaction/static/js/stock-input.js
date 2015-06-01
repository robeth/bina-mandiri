var StockInput = function(container, options){
	
	/**
	 * Stock counter (number of row)
	 */
	var stockCounter = $('<input/>', {
		type: "hidden",
		id: options.counterName,
		name: options.counterName
	});

	var tableHeaderFactory = function(){
		var tableHeader = $('<thead/>');
		var headerRow = $('<tr/>');

		function createHeaderCell(text){
			return $('<td/>', { 'text': text, 'class' : 'center'});
		}
		
		var headerCells = jQuery.map(['Kode', 'Kategori', 'Unit', 'Harga', ''], createHeaderCell);

		for(var i = 0; i < headerCells.length; i++){
			headerRow.append(headerCells[i]);
		}
		tableHeader.append(headerRow);
		return tableHeader;
	};

	var stockCodeFactory =  function(){
		return $('<code/>', {
				text: "-"
			});
	}

	var autocompleteFactory = function(){
		var stockAutocomplete = new StockAutocomplete(options.autoComplete);
		var result = { 
			'html': $(stockAutocomplete.html()),
			'stockAutocomplete' : stockAutocomplete
		}; 
		return result; 
	};

	var priceFieldFactory = function(initialPrice){
		initialPrice = typeof initialPrice !== 'undefined' ? initialPrice : "";
		return ($('<input/>', {
					type: "text",
					name: options.fields.price["name"],
					placeholder: "harga satuan",
					"class": "form-control",
					value: initialPrice
				}));
	};

	var amountFieldFactory = function(initialAmount){
		initialAmount = typeof initialAmount !== 'undefined' ? initialAmount : "";
		return $('<div/>', { "class": "input-group"})
					.append($('<input/>', {
						type: "text",
						name: options.fields.amount["name"],
						placeholder: "jumlah",
						"class": "form-control",
						value: initialAmount
					}))
					.append($('<div/>', {
						"class": "input-group-addon",
						text: "-"
					}));
	};

	function removeButtonFactory(target){
		var component = $('<button/>', {
			"class" : "btn btn-danger",
			click: function(){ $(target).remove(); }
		}).append($('<span/>', { "class" : "glyphicon glyphicon-remove"}));

		return component;
	}

	container.append(stockCounter);
	container.append(tableHeaderFactory());

	options.autoComplete.onStockUpdate = function(autoCompleteUi, newStock){
		var singleFieldContainer = autoCompleteUi.closest("tr.single-field")
		$(singleFieldContainer).find("code").first().text(newStock.kode);
		
		if(options.fields.price){
			$(singleFieldContainer).find("input[name*='"+options.fields.price["name"]+"']").attr("placeholder", "stabil: " + newStock.stabil);
		}
		
		if(options.fields.amount)
			$(singleFieldContainer).find("input[name*='"+options.fields.amount["name"]+"']").next().text(newStock.satuan);
	};

	function getInputDiv(data) {
		var rowField = $('<tr/>', {
			"class": "single-field",
		});

		function wrapCell(element){
			return $('<td/>').append(element);
		}

		var rowElements = []

		rowElements.push(stockCodeFactory());

		stockAutocompleteInstance = autocompleteFactory(); 
		rowElements.push(stockAutocompleteInstance.html);

		if(options.fields.amount)
			rowElements.push(amountFieldFactory(data['jumlah']));

		if(options.fields.price)
			rowElements.push(priceFieldFactory(data['harga']));
		
		// Init autocomplete field after all other components are loaded
		if(!$.isEmptyObject(data)){
			stockAutocompleteInstance.stockAutocomplete.forceUpdate(data);
		}

		rowElements.push(removeButtonFactory(rowField))

		var rowCells = jQuery.map(rowElements, wrapCell);
		for(var i = 0; i < rowCells.length; i++){
			rowField.append(rowCells[i]);
		}

		return rowField;
	}

	function addNewRow(data){
		$(getInputDiv(data)).fadeIn('slow').appendTo(container);
	}

	$(options.addButton).click(addNewRow);

	if(options.initial){
		for(var j = 0; j < options.initial.length; j++){
			addNewRow(options.initial[j]);
		}
	} else {
		addNewRow(new Object());
	}


    $(options.form).submit(function(e){
    	var tableRow = $(container).find('tr.single-field');
    	stockCounter.val(tableRow.length);

    	$(tableRow).each(function(index, element){
    		$(element).find('input').each(function(i, e){
    			var name = e.name.replace(/\d+$/i, "");
    			if(name && name.length > 0){
    				$(e).attr('name', name+(index+1));
    			}
    		});
    	});
    	return true;
    });

}