(function($) {
	'use strict';
	$(document).ready(function() {
		/*==== Filters ====*/

		if($("#filters-summary").length == 0) {
			$( "#changelist-filter h2" ).append( " <span id='filters-summary'></span>" );
		}

		var filtersList = [], liText, liLabel;

		$("#changelist-filter li.selected").each(function() {
			liText = $.trim($(this).text());
			liLabel = $.trim($(this).parent("ul").prev("h3").eq(0).text());

			if ($.trim(liText) != "All") {
				filtersList.push(liLabel + ": " + liText);
			}
		})

		var arrayLength = filtersList.length;

		if (arrayLength) {
			for (var i = 0; i < arrayLength; i++) {
				$("#filters-summary").text ($("#filters-summary").text() + filtersList[i]);

				if ((arrayLength >= 2) && (i != (arrayLength - 1))) {
					$("#filters-summary").text ($("#filters-summary").text() + ". ");
				}
			}
		}

		/*==== Collapsible list ====*/

		var changelist_filter;
		var changelist_filter_h2;
		var changelist_filter_h2_height;

		$(window).on("load resize", function() {

			$("#changelist-filter:not(.open)").each(function() {
				changelist_filter = $(this);

				if ($(window).width() <= 767) {
					var changelist_filter_h2 = changelist_filter.find("h2").eq(0);
					var changelist_filter_h2_height = changelist_filter_h2.outerHeight();

					changelist_filter.css("height", changelist_filter_h2_height);
					changelist_filter.css("order", 1);

				}
				else {
					changelist_filter.css("height", "");
				}
			})
		});

		$('#changelist-filter h2').on("click", function() {
			if ($(window).width() <= 767) {
				changelist_filter = $(this).parents("#changelist-filter").eq(0);
				changelist_filter_h2 = changelist_filter.find("h2").eq(0);
				changelist_filter_h2_height = changelist_filter_h2.outerHeight();
				console.log(changelist_filter[0]);
				if (changelist_filter.hasClass("open")) {
					console.log('entro en hasclass');
					changelist_filter.css("height", changelist_filter_h2_height);
				}
				else {
					changelist_filter.css("height", "auto");
					var changelist_filter_height = changelist_filter.css("height");

					changelist_filter.css("height", changelist_filter_h2_height);

					changelist_filter.animate({
						height: changelist_filter_height
					}, 30, "linear");
				}

				changelist_filter.toggleClass("open");
			}
		});

		/*==== Table resizing ====*/

		// Add the .nowrap class only to the cells containing more than 20 characters, instead of adding it to foreign key and date/time columns.
		// Add a min-width to the cells containing 20 or less characters.

		tableResizing();

		$(window).on("resize", function() {
			tableResizing();
		});


		// Add 'outside click dismiss' feature, useful for mobile.
		window.addEventListener("load", function() {
			let classes = {'.calendarbox': 'DateTimeShortcuts.dismissCalendar(num)'
							, '.clockbox': 'DateTimeShortcuts.dismissClock(num)'};
			for (let c in classes){
				$(c).on('click', function(e){
					let num = this.id.substr(c.length - 1);
					if (e.target.id === ''){
						return 0;
					} else {
						e.preventDefault();
						eval(classes[c]);
					}
				});
			}

		});


		function tableResizing() {
			$(".results table td.nowrap").removeClass("nowrap");

			var addNoWrap = [];
			var uniqueAddNoWrap = [];

			var addMinWidth = [];
			var uniqueAddMinWidth = [];

			$(".results table").each(function() {
				$(this).find("th, td").each(function() {
					if (($.trim($(this).text()).length) > 0) {
						if ($.trim($(this).text()).length < 20) {
							var noWrapClasses = $(this).attr('class');
							var noWrapClassesParsed = "." + noWrapClasses.replace(" ", ".");
							addNoWrap.push(noWrapClassesParsed);
						}
						else {
							var minWidthClasses = $(this).attr('class');
							var minWidthClassesParsed = "." + minWidthClasses.replace(" ", ".");
							addMinWidth.push(minWidthClassesParsed);
						}
					}
				})

				// Remove duplicates

				$.each(addNoWrap, function(i, el){
					if($.inArray(el, uniqueAddNoWrap) === -1) uniqueAddNoWrap.push(el);
				});

				$.each(addMinWidth, function(i, el){
					if($.inArray(el, uniqueAddMinWidth) === -1) uniqueAddMinWidth.push(el);
				});	

				if ($(window).width() <= 767) {
					uniqueAddNoWrap.forEach(function(noWrapClasses) {
						$(noWrapClasses).addClass("nowrap");
					})

					uniqueAddMinWidth.forEach(function(minWidthClasses) {
						$(minWidthClasses).addClass("minwidth");
					})
				}
				else {
					uniqueAddNoWrap.forEach(function(noWrapClasses) {
						$(noWrapClasses).removeClass("nowrap");
					})

					uniqueAddMinWidth.forEach(function(minWidthClasses) {
						$(minWidthClasses).removeClass("minwidth");
					})
				}

				addNoWrap.length = 0;
				uniqueAddNoWrap.length = 0;

				addMinWidth.length = 0;
				uniqueAddMinWidth.length = 0;			
			})
		}
	});

	/*==== Actions on results tables ====*/

	$(".actions").each(function() {
		var actions = $(this);
		var question = $(this).find(".question").eq(0);
		var actionCounter = $(this).find(".action-counter").eq(0);
		var all = $(this).find(".all").eq(0);
		var clear = $(this).find(".clear").eq(0);

		var actionsHeight = actions.outerHeight();

		question.css("display", "inline");
		var actionsQuestionHeight = actions.outerHeight();
		question.css("display", "none");

		actionCounter.css("display", "none");

		all.css("display", "inline");
		clear.css("display", "inline");

		var actionsAllClearHeight = actions.outerHeight();

		if ((actionsQuestionHeight > actionsHeight) || (actionsAllClearHeight > actionsHeight)) {
			actionCounter.addClass("two_lines");
			all.addClass("two_lines");
		}

		all.css("display", "");
		clear.css("display", "");

		actionCounter.css("display", "inline");
	});

})(django.jQuery);
