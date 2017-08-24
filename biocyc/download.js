var tree;
var output=" hello ";



function download() {
  var i;
/*
  for(i=0; i < 2;  i++) {
    var href="http://bioinformatics.ai.sri.com/ecocyc/dist/flatfiles-52983746/" + samples[i]
    var createA = document.createElement('a');
    var createAText = document.createTextNode(samples[i]);
    createA.appendChild(createAText);
    createA.setAttribute('href', href);
    createA.setAttribute('id', samples[i]);
    document.body.appendChild(createA);                    // Append <button> to <body>
  }
  for(i=0; i < 2;  i++) {
     document.getElementById(samples[i]).click() ;
  }
*/

  var filesForDownload = [];


  for(i=0; i < 2;  i++) {
     var href="http://bioinformatics.ai.sri.com/ecocyc/dist/flatfiles-52983746/" + samples[i];
     filesForDownload.push({ path: href, name: samples[i] });
  }

  $jq('input.downloadAll').click( function( e )
   {
    e.preventDefault();
    var temporaryDownloadLink = document.createElement("a");
    temporaryDownloadLink.style.display = 'none';
    document.body.appendChild( temporaryDownloadLink );
    for( var n = 0; n < filesForDownload.length; n++ )
    {
        var download = filesForDownload[n];
        temporaryDownloadLink.setAttribute( 'href', download.path );
        temporaryDownloadLink.setAttribute( 'download', download.name );

        temporaryDownloadLink.click();
    }

    document.body.removeChild( temporaryDownloadLink );
   }   );

//document.body.appendChild(btn);                    // Append <button> to <body>

}

function downloadAll() {
  var link = document.createElement('a');

  var  urls=[];
  for(i=0; i < samples.length;  i++) {
     var href="http://bioinformatics.ai.sri.com/ecocyc/dist/flatfiles-52983746/" + samples[i];
     urls.push(href);
  }

  link.setAttribute('download', null);
  link.style.display = 'none';

  document.body.appendChild(link);

  for (var i = 0; i < urls.length; i++) {
    link.setAttribute('href', urls[i]);
    console.log(urls[i]);
    if( i%10==0) {
      console.log("downlading : " + i.toString());
    }
    setTimeout( link.click(), 10000);
  }

  document.body.removeChild(link);
}

function getFiles() {
    $('#download').click(function() {
       download("asp310037.tar.gz", "acel509191.tar.gz");
     });

     var download = function() {
       for(var i=0; i<arguments.length; i++) {
         console.log(arguments[i]);
         var iframe = $('<iframe style="visibility: collapse;"></iframe>');
         $('body').append(iframe);
         var content = iframe[0].contentDocument;
         var href="http://bioinformatics.ai.sri.com/ecocyc/dist/flatfiles-52983746/" + arguments[i]
         var form = '<form action="' + href + '" method="GET"></form>';
         content.write(form);
         $('form', content).submit();
         setTimeout((function(iframe) {
           return function() { 
             iframe.remove(); 
           }
         })(iframe), 10000);
       }
     }      
}


var samples = [
"bthe.tar.gz",
"ecol1001989-hmp.tar.gz",
"ecol1004153-hmp.tar.gz",
"ecol1005397.tar.gz",
"ecol1005402.tar.gz",
"ecol1005403.tar.gz",
"ecol1005404.tar.gz",
"ecol1005407.tar.gz",
"ecol1005410.tar.gz",
"ecol1005411.tar.gz",
"ecol1005412.tar.gz",
"ecol1005413.tar.gz",
"ecol1005414.tar.gz",
"ecol1005415.tar.gz",
"ecol1005418.tar.gz",
"ecol1005419.tar.gz",
"ecol1005423.tar.gz",
"ecol1005430.tar.gz",
"ecol1005433.tar.gz",
"ecol1005434.tar.gz",
"ecol1005440.tar.gz",
"ecol1005450.tar.gz",
"ecol1005455.tar.gz",
"ecol1005460.tar.gz",
"ecol1005462.tar.gz",
"ecol1005464.tar.gz",
"ecol1005467.tar.gz",
"ecol1005470.tar.gz",
"ecol1005475.tar.gz",
"ecol1005477.tar.gz",
"ecol1005478.tar.gz",
"ecol1005480.tar.gz",
"ecol1005481.tar.gz",
"ecol1005482.tar.gz",
"ecol1005483.tar.gz",
"ecol1005486.tar.gz",
"ecol1005491.tar.gz",
"ecol1005492.tar.gz",
"ecol1005495.tar.gz",
"ecol1005496.tar.gz",
"ecol1005508.tar.gz",
"ecol1005509.tar.gz",
"ecol1005522.tar.gz",
"ecol1005523.tar.gz",
"ecol1005524.tar.gz",
"ecol1005527.tar.gz",
"ecol1005528.tar.gz",
"ecol1005529.tar.gz",
"ecol1005530.tar.gz",
"ecol1005536.tar.gz",
"ecol1005541.tar.gz",
"ecol1005542.tar.gz",
"ecol1005563.tar.gz",
"ecol1005566.tar.gz",
"ecol1033813.tar.gz",
"ecol1048254.tar.gz",
"ecol1048256.tar.gz",
"ecol1048265.tar.gz",
"ecol1048689.tar.gz",
"ecol1051346.tar.gz",
"ecol1051348.tar.gz",
"ecol1051350.tar.gz",
"ecol1051353.tar.gz",
"ecol1068614.tar.gz",
"ecol1068621.tar.gz",
"ecol1072459.tar.gz",
"ecol1073985.tar.gz",
"ecol1078031.tar.gz",
"ecol1078033.tar.gz",
"ecol1078035.tar.gz",
"ecol1081887.tar.gz",
"ecol1089445.tar.gz",
"ecol1090928.tar.gz",
"ecol1101440.tar.gz",
"ecol1110693.tar.gz",
"ecol1127356-hmp.tar.gz",
"ecol1133852.tar.gz",
"ecol1133853.tar.gz",
"ecol1134782.tar.gz",
"ecol1144302.tar.gz",
"ecol1144303.tar.gz",
"ecol1163738.tar.gz",
"ecol1165949.tar.gz",
"ecol1165950.tar.gz",
"ecol1165951.tar.gz",
"ecol1165952.tar.gz",
"ecol1165953.tar.gz",
"ecol1167694-wgs.tar.gz",
"ecol1169324.tar.gz",
"ecol1169325.tar.gz",
"ecol1169328.tar.gz",
"ecol1169330.tar.gz",
"ecol1169331.tar.gz",
"ecol1169332.tar.gz",
"ecol1169336.tar.gz",
"ecol1169337.tar.gz",
"ecol1169340.tar.gz",
"ecol1169344.tar.gz",
"ecol1169356.tar.gz",
"erec.tar.gz",
"hpar1117322.tar.gz"
];
