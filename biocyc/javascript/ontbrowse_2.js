var tree;


var output="";
function download(name, type) {
  var a = document.getElementById("a");
  var file = new Blob([output], {type: type});
  a.href = URL.createObjectURL(file);
  a.download = name;
}



function classBrowser(topClass) {

var containers= [ "ontologyDiv0", "ontologyDiv1"];
var treeInitialized = false;
var biocyc = "https://biocyc.org";
var num = 0;
var samples = ["EREC", "ABAU1221271"];
//var samples = [ "EREC"];
var org; 

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

function orgID() {
  return sample;
}

function buildTree() {

 if (!treeInitialized) {
   tree = new YAHOO.widget.TreeView(containers[0]);
   var root = tree.getRoot();
   var top = new YAHOO.widget.TextNode(topClass, root, false);
   top.href = biocyc + "/" + orgID() + "/new-image?object=" + topClass;
   loadSubclasses(top);
}

}


var callback1 = {
   
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
                  href = biocyc + "/" + oResponse.argument.orgid + "/new-image?object=" + encodeURIComponent(nodeData.id);
                  var sUrl = biocyc + "/" + oResponse.argument.orgid + "/ajax-direct-subs?object=" + encodeURIComponent(nodeData.id); 
          //        console.log(oResponse.argument.orgid + " " + i.toString() + " " +  num.toString() + " " + nodeData.id); 
                  output += oResponse.argument.orgid + "\t"  + nodeData.id + "\n"; 
                  var c = callback1; 
                  c.argument.orgid = oResponse.argument.orgid;
                  YAHOO.util.Connect.asyncRequest('GET', sUrl, callback1);
                  num++;
                }
                else { 
                  var href = biocyc +  "/" + oResponse.argument.orgid + "/new-image?object=" + encodeURIComponent(nodeData.id);
           //       console.log(oResponse.argument.orgid + " " + i.toString() + "  " + num.toString() + " " + nodeData.id); 
                  if ( num%10==0)  {
                      console.log(oResponse.argument.orgid + " " + i.toString() + "  " + num.toString() + " " + nodeData.id); 
                  }
                  output += oResponse.argument.orgid + "\t" + nodeData.id + "\n"; 
                  num++;
                }
              }
            } 

         }
     },
        
     failure:  failLoadSubclasses,
        
     argument: { orgid : "", },
     //timeout -- if more than 60 seconds go by, we'll abort
     timeout: 60000
  };
    

for( i = 0; i < samples.length; i++ ) {
    sample = samples[i];
    console.log(orgID());
/*
    treeInitialized = false;

    var tree = new YAHOO.widget.TreeView(containers[i]);
    var root = tree.getRoot();
    var top = new YAHOO.widget.TextNode(topClass, root, false);

    top.href = biocyc + "/" + samples[i] + "/new-image?object=" + topClass;

    var nodeLabel = encodeURI(root.label);
    if (root.data.id) {
      nodeLabel = root.data.id;
     }
*/

    var topClass="Pathways";
    var sUrl = biocyc + "/" + samples[i] + "/ajax-direct-subs?object=" + encodeURI(topClass); 
  
    var c = callback1; 
    c.argument.orgid = samples[i];
    YAHOO.util.Connect.asyncRequest('GET', sUrl, callback1);
 }


}

function failLoadSubclasses (oResponse) {
  YAHOO.log("Failed to process XHR transaction.", "info", "loadSubclasses");
  oResponse.argument.fnLoadComplete();
}
