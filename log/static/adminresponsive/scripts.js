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
				if (changelist_filter.hasClass("open")) {
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
	});
})(django.jQuery);
