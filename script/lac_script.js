var browserType;

if (document.layers) {browserType = "nn4"}
if (document.all) {browserType = "ie"}
if (window.navigator.userAgent.toLowerCase().match("gecko")) {
   browserType= "gecko"
}

function showhide(id) {
	
  if (browserType == "gecko" )
     document.poppedLayer =
         eval('document.getElementById(id)');
  else if (browserType == "ie")
     document.poppedLayer =
        eval('document.getElementById(id)');
  else
     document.poppedLayer =
        eval('document.layers[id]');
          
  if (document.poppedLayer.style.display == "none") 
  	document.poppedLayer.style.display = "inline";
  else
  	document.poppedLayer.style.display = "none";
}

 function onChangeDateSelect(dropDown)
 {
 	//alert(dropDown.name == "startDateSelect");
 	
 	if (dropDown.name == "startDateSelect")
 	{
 		//alert(document.schedule.endDateSelect.selectedIndex);
 		document.schedule.endDateSelect.selectedIndex = dropDown.selectedIndex + 1; 	
 	}
 	else if (dropDown.name == "endDateSelect")
 	{
 		//alert("endDateSelect");
 	}
 	else
 	{
 		//alert(dropDown.name);
 	}
 }