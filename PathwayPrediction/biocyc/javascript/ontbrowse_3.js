var tree;
var output=" hello ";

function download(name, type) {
  var file = new Blob([output], {type: type});
  var loc = URL.createObjectURL(file);

  document.getElementById('myfile').name = name;
  document.getElementById('myfile').value = loc;

  document.getElementById("myform").submit();
  console.log("hi");

}



function classBrowser(topClass) {
var treeInitialized = false;
var biocyc = "https://biocyc.org";
var num = 0;
var samples = getSamples();
var k=0;
//var samples = [ "EREC",  "ABAU1221271"];
var org; 

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e14; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

function failLoadSubclasses (oResponse) {
  YAHOO.log("Failed to process XHR transaction.", "info", "loadSubclasses");
  console.log("Failed to connect " );
  k--;

  console.log("restarting....." + samples[k]);
  var topClass="Pathways";
  var sUrl = biocyc + "/" + samples[k] + "/ajax-direct-subs?object=" + encodeURI(topClass); 
  var call = createCallback(); 
  call.argument.orgid = samples[k];
  counter[k]= 0;
  k++;
  YAHOO.util.Connect.asyncRequest('GET', sUrl, call);
}

function createCallback() {

     return  {
     success: function(oResponse) {
       YAHOO.log("XHR transaction was successful.", "info", oResponse.responseText);
       var oResults = eval("(" + oResponse.responseText + ")");

       if((oResults) && (oResults.length)) {
            //Result is an array if more than one result, string otherwise
            if(YAHOO.lang.isArray(oResults)) {
                if (oResults.length > 0) {
                    counter[oResponse.argument.k] -= 1;
                }
                for (var i=0, j=oResults.length; i<j; i++) {
                    var nodeData = oResults[i];
                    if (nodeData.isClass) {
                       href = biocyc + "/" + oResponse.argument.orgid + "/new-image?object=" + encodeURIComponent(nodeData.id);
                       var sUrl = biocyc + "/" + oResponse.argument.orgid + "/ajax-direct-subs?object=" + encodeURIComponent(nodeData.id); 
                       output += oResponse.argument.orgid + "\t"  + nodeData.id + "\n"; 
                       var c = createCallback(); 
                       c.argument.orgid = oResponse.argument.orgid;
                       counter[oResponse.argument.k] += 1;
                       try{
                         YAHOO.util.Connect.asyncRequest('GET', sUrl, c);
                       } catch(err) {
                             console.log("ERROR: " + err);
                       }
                      // console.log("counter : " + counter.toString());
                       num++;
                    }
                    else { 
                       var href = biocyc +  "/" + oResponse.argument.orgid + "/new-image?object=" + encodeURIComponent(nodeData.id);
                       output += oResponse.argument.orgid + "\t" + nodeData.id + "\n"; 
                       num++;
                       //console.log("ccounter : " + counter.toString());
    
                       if( counter[oResponse.argument.k]==0 && k < samples.length ) {
                          console.log(k.toString() + "  " + samples[k] );
                          var topClass="Pathways";
                          var sUrl = biocyc + "/" + samples[k] + "/ajax-direct-subs?object=" + encodeURI(topClass); 
                          var call = createCallback(); 
                          call.argument.orgid = samples[k];
                          counter[oResponse.argument.k] += 1;
                          k++;
                          try{
                             YAHOO.util.Connect.asyncRequest('GET', sUrl, call);
                          } catch(err) {
                             console.log("ERROR: " + err);
                          }
                       }

                    }
               }
            }
            else { 
                 console.log("not an array counter : " + counter.toString());
            }
       }
     },
        
     failure:  failLoadSubclasses,
        
     argument: { orgid : "", k:0 },
     //timeout -- if more than 60 seconds go by, we'll abort
     timeout: 60000
    };

}
    


download("hello.txt", "text/plain");
var counter = new Array();
for( i = 0; i < samples.length; i++ ) {
   counter.push(0)
}

console.log(samples[k]);
var topClass="Pathways";
var sUrl = biocyc + "/" + samples[k] + "/ajax-direct-subs?object=" + encodeURI(topClass); 
var call = createCallback(); 
call.argument.orgid = samples[k];
counter[k] += 1;
k++;
//YAHOO.util.Connect.asyncRequest('GET', sUrl, call);


console.log("Waking up================>\n");

}

