// Admin index: filter specific apps by a date param.
django.jQuery(document).ready(function($){
	
	var date_querystring = function(param){
		var now = new Date();
		var day_first = new Date(now.getFullYear(), now.getMonth(), 1);
		var day_last = new Date(now.getFullYear(), now.getMonth() + 1, 0);
		day_last.setDate(day_last.getDate() + 1);
		var day_first = day_first.getFullYear() + '-' + ("0" + (day_first.getMonth() + 1)).slice(-2) + '-01';
		var day_last = day_last.getFullYear() + '-' + ("0" + (day_last.getMonth() + 1)).slice(-2) + '-01';

		return '?' + param + '__gte=' + day_first + '&' + param + '__lt=' + day_last;
	}

	if($('body').hasClass('dashboard')) {
		var app_params = {
			/* The format for this list is:
			   { 
			     'app_slug/optional_model': 'created_at',
			   }
			   To exclude a specific model from filtering, list it before the app, 
			   and set it to 'false':
			   { 
			     'app_slug/unfiltered_model': false,
				 'app_slug': 'created_at',
			   }
			 */
			'log/entry' : 'date',	
		};
		
		$(this).find('div.module tbody a').each(function(){

			var href = $(this).attr('href');

			for (var key in app_params){
				if (href.indexOf(key + "/") > -1){
					if (app_params[key]){
						$(this).attr('href', href + date_querystring(app_params[key]));
					}
					break;
				}
			}

		})

	}
})


