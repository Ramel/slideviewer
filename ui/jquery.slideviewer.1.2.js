/*!
 * slideViewer 1.2.1
 * Modified 2010 Armel FORTUN
 * slideViewer 1.2
 * Examples and documentation at:
 * http://www.gcmingati.net/wordpress/wp-content/lab/jquery/imagestrip/imageslide-plugin.html
 * 2007-2010 Gian Carlo Mingati
 * Version: 1.2.3 (9-JULY-2010)
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 *
 * Requires:
 * jQuery v1.4.1 or later, jquery.easing.1.2
 *
 */

jQuery(function(){
	jQuery("div.svw").prepend("<div style='text-align:center' class='ldrgif'><img style='margin-top:150px' src='./lib/loadingAnimation.gif' alt='Chargement...'/ ></div>");
	//jQuery("div.svw").prepend("<img src='spinner.gif' class='ldrgif' alt='loading...'/ >");
});
var j = 0;
var quantofamo = 0;
jQuery.fn.slideView = function(settings) {
	settings = jQuery.extend({
		easeFunc: "easeInOutExpo",
		easeTime: 750,
		uiBefore: false,
		toolTip: false,
		ttOpacity: 0.9
	}, settings);
	return this.each(function(){
		var container = jQuery(this);
		container.find("div.ldrgif").remove();
		container.removeClass("svw").addClass("stripViewer").attr({style: "text-align:center"});
		var pictWidth = container.find("li").find("img").width();
		var pictHeight = container.find("li").find("img").height();
		var pictEls = container.find("li").size();
		// Find the larger image
		var maxi = 0;
		for(i=0; i<pictEls; i++) {
			var imgWidth = container.parent().find("ul").find("li").eq(i).find("img").width();
			if(imgWidth > maxi) { pictWidth = imgWidth; }
			maxi =  pictWidth;
		}
		// Add style for first A tag, that give the dimension to the SV
		jQuery(this).parent().find("ul").find("li").eq(0).find("a").attr({ style: "width:"+pictWidth+"px;display:block;"});
		// Add a line-height, used with a vertical-align:middle the images in the SV
		jQuery(this).parent().find("ul").find("li").find("a").css({ "line-height": pictHeight+"px"});
		// Get the square color
		var square = jQuery(this).parent().find("ul").attr("class");
		jQuery(this).parent().find("ul").removeAttr("class");
		//console.log(square);
		//jQuery(this).parent().find("DIV#stripTransmitter" + j + " A").css("background-color", square);
		var stripViewerWidth = pictWidth*pictEls;
		var imageWidth = new Array();
		container.find("ul").css("width" , stripViewerWidth);
		container.css("width" , pictWidth);
		container.css("height" , pictHeight);
		container.each(function(i) {
			(!settings.uiBefore) ? jQuery(this).after("<div class='stripTransmitter' id='stripTransmitter" + (j) + "'><ul><\/ul><\/div>") : jQuery(this).before("<div class='stripTransmitter' id='stripTransmitter" + (j) + "'><ul><\/ul><\/div>");
			jQuery(this).find("li").each(function(n) {
				//jQuery("DIV#stripTransmitter" + j + " A").css("background-color", square);
				jQuery("div#stripTransmitter" + j + " ul").append("<li><a title='" + jQuery(this).find("img").attr("alt") + "' href='#'>"+(n+1)+"<\/a><\/li>");
				imageWidth[n] = jQuery(this).find("img").attr("width");
			});
			// Need to add color to .current
			//jQuery("DIV#stripTransmitter" + j + " A").hasClass("current").css("background-color", "#fff");
			jQuery("div#stripTransmitter" + j + " a").each(function(z) {
				jQuery(this).bind("click", function(){
					//jQuery(this).parent().parent().find("A").css("background-color", square);
					jQuery(this).addClass("current").parent().parent().find("a").css("background-color","#fff").not(jQuery(this)).removeClass("current").css("background-color", square); // wow!
					///////////////////
					// If the image's width is smaller than pictWidth,
					// We resize the A tag to the pictWidth's size
					if(imageWidth[z] < pictWidth) {
						// Add a new width to the A tag and display it as a block.
						jQuery(this).parent().parent().parent().prev().find("ul").find("li").eq(z).find("a").attr({ style: "width:"+pictWidth+"px;display:block"});
						// Change the pictWidth to the new A size
						imageWidth[z] = pictWidth;
					} else if (imageWidth[z] > pictWidth) {
						imageWidth[z] = pictWidth;
						jQuery(this).parent().parent().parent().prev().find("ul").find("li").eq(z).find("a").attr({ style: "width:"+pictWidth+"px;display:block;overflow:none;"});
					}
					// Create a new Array, and slice it at the actual position
					var temp = new Array();
					temp = imageWidth.slice(0,z);
					var cnt = 0;
					for(var i=0; i<temp.length; i++) {
						// If the first image is smaller than the maxi image
						if((imageWidth[i] < maxi) && (i==0)) {
							cnt = Number(maxi)+cnt;
						} else {
							cnt = Number(imageWidth[i])+cnt;
						}
					}
					jQuery(this).parent().parent().parent().prev().find("ul").animate({ left: -cnt}, settings.easeTime, settings.easeFunc);
					return false;
				});
			});
			// Next image via image click : 14/01/2009
			// 15/10/2010: Added a parent() to 'ui' var
			jQuery("div#stripTransmitter" + j + " a").parent().parent().parent().prev().find("img").each(function(z) {
				jQuery(this).bind("click", function(){
					var ui = jQuery(this).parent().parent().parent().parent().next().find("a");
					if(z+1 < pictEls){
						ui.eq(z+1).trigger("click");
					}
					else ui.eq(0).trigger("click");
				});
			});
			jQuery("div#stripTransmitter" + j).css("width" , pictWidth);
			jQuery("div#stripTransmitter" + j + " a:first(0)").addClass("current");
			jQuery('body').append('<div class="tooltip" style="display:none;"><\/div>');


			if(settings.toolTip){
				var aref = jQuery("div#stripTransmitter" + j + " a");

				aref.live('mousemove', function(e) {
					var att = jQuery(this).attr('title');
					posX=e.pageX+10;
					posY=e.pageY+10;
					jQuery('.tooltip').html(att).css({'position': 'absolute', 'top': posY+'px', 'left': posX+'px', 'display': 'block', 'opacity': settings.ttOpacity});
				});
				aref.live('mouseout', function() {
					jQuery('.tooltip').hide();
				});
			}
		});
		j++;
	});
};
