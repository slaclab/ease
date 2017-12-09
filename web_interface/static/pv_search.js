//Copied from M. Shankar's svg_viewer and hacked a bit by A. Wallace

// viewerVars is a struct that contains all the information needed for the viewer;
// To debug, a useful first step is look at viewerVars in the browser console.
var viewerVars = {};// This is one of the integration points with the server.

// This should default to a path relative location that works from the appliance UI.
// To develop/debug, override this to a absolute URL of the server with the data you are going to use for debugging/developing.
viewerVars.serverURL = "https://pswww.slac.stanford.edu/archiveviewer/retrieval";
//Set up an ssh tunnel to pslogin -L 8700:pswww.slac.stanford.edu:80
//viewerVars.serverURL = "http://localhost:8700/archiveviewer/retrieval";//remote work with port forwarding

// User typed a pattern, we search for PV's matching this pattern.
function searchForPVsMatchingPattern(pvNamePattern) {
	if (pvNamePattern == null){
		var pattern = $("#pvNamePattern").val();
	}
	else{
		var pattern = pvNamePattern;
	}	
	var globp = /[\*\?]/;
	if(!globp.test(pattern)) {
		console.log(pattern + " is not a glob pattern");
		$("#pvSearchWidget-container box1 info-container nameSearchMatchingError").html(pattern + " is not a glob pattern");
		return;
	}
	if(pattern) {
		console.log("Search and add PVs for pattern " + pattern);
		console.log("URL "+viewerVars.serverURL);
		var list = $("#pvNameSearchMatchingList");
		list.empty();
		$("#pvSearchWidget-container box1 info-container nameSearchMatchingError").empty();
		$.getJSON( viewerVars.serverURL + "/bpl/getMatchingPVs?limit=50&pv=" + pattern, function(matchingPVs){
			
			if(matchingPVs.length > 0) {
				matchingPVs.forEach(function(matchingPV) { list.append('<li class="list-group-item">' + matchingPV + '</li>') });
				$("#pvNameSearchMatchingList li").click(function() { $(this).toggleClass('list-group-item-info'); });
				return;
			} else {
				$("#pvSearchWidget-container box1 info-container nameSearchMatchingError").html("No PV names matched your search. Search using GLOB patterns, for example, QUAD:*:BDES");
			}
		});
	}
}

function addSelectedSearchPVs(e) {
	var triggerPVList = $("#triggerPVList");
	$("#pvNameSearchMatchingList li.list-group-item-info").each(function() { triggerPVList.append('<li class="list-group-item">' + $(this).text() + '</li>')});
	$("#triggerPVList li").click(function() { $(this).toggleClass('list-group-item-info'); });
	$("#pvNameSearchMatchingList li.list-group-item-info").each(function() { $(this).remove() });
}

function addAllSearchPVs() {
	var triggerPVList = $("#triggerPVList");
	$("#pvNameSearchMatchingList li").each(function() { triggerPVList.append('<li class="list-group-item">' + $(this).text() + '</li>')});
	$("#pvNameSearchMatchingList").empty();
}

function removeSelectedTriggerPVs () {
	$("#triggerPVList li.list-group-item-info").each(function() { $(this).remove() });
}

function removeAllTriggerPVs () {
	$("#triggerPVList").empty();
}

function populateTriggerPVs() {

}

function saveTriggerPVs() {
	var triggerPVList = $("#triggerPVList li");
	var seen = {};
	triggerPVList.each(function() {
		var txt = $(this).text();
		if (seen[txt])
			$(this).remove();
		else
			seen[txt] = true;
	});
	//console.log(triggerPVList.length());
	var list = [];
	triggerPVList.each(function() { console.log(this.text()) });
	if(triggerPVList.length > 0) { 
		$("#"+pvTagId).val(list);
	 }
	 $("#triggerPVList").empty();
}