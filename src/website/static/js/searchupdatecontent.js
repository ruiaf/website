Event.observe(window, 'load', function() {
	Event.observe('searchform','submit',search_ajah,false);
})

function search_ajah(e) {
	Event.stop(e);
	new Ajax.Updater('content','/', {
				method:'post',
				parameters: { xhr: true, search: $('searchquery').value } 
  	});
}

