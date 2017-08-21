/**************************************************************************
 * Class Browser widget
 * container: the id of the div element for the tree
 * topClass: the id of the class frame which is the root of the tree
 * module: the module containing the class browser.  We subscribe to the show
 *         event for this module so that we only build the tree when the module
 *         is shown.  The resulting tree is stored in the trees[] array, with
 *         the module as the key.
 */
var tree;



function classBrowser(topClass) {

var container= "ontologyDiv";
var treeInitialized = false;
var biocyc = "https://biocyc.org";
var num = 0;
//var samples = ["EREC", "ABAU1221271"];
var samples = [ "EREC"];
var org; 



function orgID() {
  return sample;
}

function buildTree() {
 if (!treeInitialized) {
   //create a new tree:
   tree = new YAHOO.widget.TreeView(container);
   
   //turn dynamic loading on for entire tree:
   tree.setDynamicLoad(loadSubclasses, 1);
   
   //get root node for tree:
   var root = tree.getRoot();
   var top = new YAHOO.widget.TextNode(topClass, root, false);
   top.href = biocyc + "/" + orgID() + "/new-image?object=" + topClass;

   console.log(top.label);
   tree.draw();
   //top.expand();
  // treeInitialized = true;
}}


function loadSubclasses(node, fnLoadComplete) {
  var nodeLabel = encodeURI(node.label);
  if (node.data.id) {
    nodeLabel = node.data.id;
  }
  var sUrl = biocyc + "/" + orgID() + "/ajax-direct-subs?object=" + nodeLabel; 
  //prepare our callback object
  var callback = {
   
     //if our XHR call is successful, we want to make use
     //of the returned data and create child nodes.
     success: function(oResponse) {
       YAHOO.log("XHR transaction was successful.", "info", oResponse.responseText);
       var oResults = eval("(" + oResponse.responseText + ")");
         if((oResults) && (oResults.length)) {
            //Result is an array if more than one result, string otherwise
            if(YAHOO.lang.isArray(oResults)) {
              for (var i=0, j=oResults.length; i<j; i++) {
                var nodeData = oResults[i];
                if (nodeData.isClass) {
                  var tempNode = new YAHOO.widget.TextNode(nodeData, node, false);
                  tempNode.data = nodeData;
		          tempNode.label = nodeData.label + " (" + nodeData.numInstances + " instances)";
	              tempNode.href = biocyc + "/" + orgID() + "/new-image?object=" + encodeURIComponent(tempNode.data.id);
		          tempNode.isLeaf = (nodeData.numInstances == 0);
                  console.log(i.toString() + " " +  num.toString() + " " + tempNode.label); 
                  num++;
		  // If there is only one child, don't make the user keep
 		  // clicking -- just keep expanding until we get to a choice
		  // or a leaf.
                 // if (oResults.length == 1) 
                //  tempNode.expand();
                }
                else { 
                  var tempNode = new YAHOO.widget.TextNode(nodeData, node, false);
                  tempNode.data = nodeData;
	            tempNode.href = biocyc +  "/" + orgID() + "/new-image?object=" + encodeURIComponent(tempNode.data.id);
                  //tempNode.target = window.opener;
                  tempNode.isLeaf = true;
                  console.log( i.toString() + "  " + num.toString() + " " + tempNode.label); 
                  num++;
                }
              }
            } else {
                //there is only one result; comes as string:
                var tempNode = new YAHOO.widget.TextNode(oResults, node, false, false)
                if (!tempNode.isClass) {
                  tempNode.isLeaf = true;
                  console.log( i.toString() +  " " + num.toString() + " " + tempNode.label); 
                  num++;
                } 
            }
         }
                                
         //When we're done creating child nodes, we execute the node's
         //loadComplete callback method which comes in via the argument
         //in the response object (we could also access it at node.loadComplete,
         //if necessary):
         oResponse.argument.fnLoadComplete();
     },
        
     //if our XHR call is not successful, we want to
     //fire the TreeView callback and let the Tree
     //proceed with its business.
     failure:  failLoadSubclasses,
        
     //our handlers for the XHR response will need the same
     //argument information we got to loadNodeData, so
     //we'll pass those along:
     argument: {
        "node": node,
        "fnLoadComplete": fnLoadComplete
     },
        
     //timeout -- if more than 60 seconds go by, we'll abort
     //the transaction and assume there are no children:
     timeout: 60000
  };
    
  //With our callback object ready, it's now time to 
  //make our XHR call using Connection Manager's
  //asyncRequest method:
  YAHOO.util.Connect.asyncRequest('GET', sUrl, callback);
}

for( i = 0; i < samples.length; i++ ) {
    sample = samples[i];
    console.log(orgID());
    treeInitialized = false;
    YAHOO.util.Event.onDOMReady(buildTree);

    document.getElementById(container).innerHTML = "";

    delete tree;

}




}

function failLoadSubclasses (oResponse) {
  YAHOO.log("Failed to process XHR transaction.", "info", "loadSubclasses");
  oResponse.argument.fnLoadComplete();
}
