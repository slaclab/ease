//Copied from M. Shankar's svg_viewer

// viewerVars is a struct that contains all the information needed for the viewer;
// To debug, a useful first step is look at viewerVars in the browser console.
var viewerVars = {};// This is one of the integration points with the server.

// This should default to a path relative location that works from the appliance UI.
// To develop/debug, override this to a absolute URL of the server with the data you are going to use for debugging/developing.
viewerVars.serverURL = "https://pswww.slac.stanford.edu/archiveviewer/retrieval";
viewerVars.serverURL = "http://localhost:8700/archiveviewer/retrieval";//remote work with port forwarding

// User typed a pattern, we search for PV's matching this pattern.
function searchForPVsMatchingPattern() {
	var pattern = $("#pvNamePattern").val();
	var globp = /[\*\?]/;
	if(!globp.test(pattern)) {
		$('#searchAndAddPVsModal').modal('hide');
		console.log(pattern + " is not a glob pattern");
		addTraceForNewPVs([pattern]);
		return;
	}
	if(pattern) {
		console.log("Search and add PVs for pattern " + pattern);
		console.log("URL"+viewerVars.serverURL);
		var list = $("#pvNameSearchMatchingList");
		list.empty();
		$("#pvNameSearchMatchingError").empty();
		$.getJSON( viewerVars.serverURL + "/bpl/getMatchingPVs?limit=50&pv=" + pattern, function(matchingPVs){
			if(matchingPVs.length > 0) {
				matchingPVs.forEach(function(matchingPV) { list.append('<li class="list-group-item">' + matchingPV + '</li>') });
				$("#pvNameSearchMatchingList li").click(function() { $(this).toggleClass('list-group-item-info'); });
			} else {
				$("#pvNameSearchMatchingError").html("No PV names matched your search. Search using GLOB patterns, for example, QUAD:*:BDES");
			}
		});
	}
}