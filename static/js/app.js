console.log("aap.js loaded");
// base.html required JS 
function myAction_vender(id) {
  document.getElementById("myForm").action = "/select_vender";
  document.getElementById("myForm").submit();
}
function myAction_dept() {
  document.getElementById("myForm").action = "/select_dept";
  document.getElementById("myForm").submit();
}
function myAction_logout() {
  document.getElementById("myForm").action = "/logout";
  document.getElementById("myForm").submit();
}

// parameter.html required JS functions

function show_no() {
  //document.getElementById("myForm").action = "/save_reading";
  var x = document.getElementById("myForm3").elements.length;
  var y = document.getElementById("myForm3").elements.item(4).value;
  var z = document.getElementById("myForm3").elements.namedItem("Remarks")
    .value;
  alert(x + y + z);
}
function getAllValues() {
  var x = document.getElementById("myForm3");
  var txt = "";
  var i;
  for (i = 0; i < x.length; i++) {
    txt = txt + x.elements[i].value + "|";
  }
  alert(txt);
  ////document.getElementById("myForm").element.namedItem("Remarks") = txt;
  document.getElementById("textall").value = txt;
  return txt;
}
