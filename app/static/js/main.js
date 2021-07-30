function goBack() {
  window.history.back();
}

function formSubmit(a) {
  if (document.getElementById(a).value == 'asc') {
    document.getElementById(a).value = 'desc';
    document.getElementById("managerForm").submit();
  } else {
    document.getElementById(a).value = 'asc';
    document.getElementById("managerForm").submit();
  }
}

function delUser() {
  if (confirm("削除しますが、よろしいでしょうか。"))
    return document.getElementById("formSubmit").submit();
  else
    return false;
}

function checkDate(){
  var startList = new Array();
  $(".date_start").each(function(index, el) {
    startList[index] = el.value;
  });
  var endList = new Array();
  $(".date_end").each(function(index, el) {
    endList[index] = el.value;
  });
  for (let i = 0; i < startList.length; i++) {
    if (startList[i] > endList[i]){ 
      $("#dateErr label").text("「失効日」は「交付年月日」より未来の日で入力してください。")
      return false;
    }
  }
  return true;
}

function addRequired(a){
  if ($('#device'+a).val() != ''){
    $('#date_start'+a).attr('required',true);
    $('#date_end'+a).attr('required',true);
  }
  else {
    $('#date_start'+a).attr('required',false);
    $('#date_end'+a).attr('required',false);
  }
}

$(document).ready(function () {
  $("#loadbutton").click(function () {
    $("#box").load("/abc");
  });
});


