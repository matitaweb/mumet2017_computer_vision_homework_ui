
/* global $, window */

function updateImage(nameImage){
    
    $('#merged_result').html('<img id="example" src="' + nameImage + '" />');
    $('img#example').selectAreas({
					minSize: [10, 10],
					onChanged: debugQtyAreas,
					maxAreas:2,
					areas: [
						{
							x: 10,
							y: 20,
							width: 60,
							height: 100,
						}
					]
				});
    
}

function areaToString (area) {
	return (typeof area.id === "undefined" ? "" : (area.id + ": ")) + area.x + ':' + area.y  + ' ' + area.width + 'x' + area.height + '<br />'
}



// Log the quantity of selections
function debugQtyAreas (event, id, areas) {
	console.log(areas.length + " areas", arguments);
	displayAreas(areas);
};

// Display areas coordinates in a div
function displayAreas (areas) {
	var text = "";
	if(areas.length >0){
	    var a1 = areas[0];
    	$('input[name=x11]').val(a1.x);
    	$('input[name=y11]').val(a1.y);
    	$('input[name=x12]').val(a1.x + a1.width);
    	$('input[name=y12]').val(a1.y+ a1.height);
    	$('input[name=area1]').val(a1.width* a1.height);
	}
	
	
	if(areas.length >1){
    	var a2 = areas[1];
    	$('input[name=x21]').val(a2.x);
    	$('input[name=y21]').val(a2.y);
    	$('input[name=x22]').val(a2.x + a2.width);
    	$('input[name=y22]').val(a2.y+ a2.height);
    	$('input[name=area2]').val(a2.width* a2.height);
	}

	console.log(text);
	
	
};
			
$(function () {
    'use strict';

});
