function goBack() {
  window.history.back();
}


function change(a) {
  if (document.getElementById(a).value == '⌄') {
    document.getElementById(a).value = '⌃';
    document.getElementById("managerForm").submit();
  } else {
    document.getElementById(a).value = '⌄';
    document.getElementById("managerForm").submit();
  }
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
  if (confirm("MSG004: 削除しますが、よろしいでしょうか。"))
    return document.getElementById("formSubmit").submit();
  else
    return false;
}

$(document).ready(function () {
  $("#loadbutton").click(function () {
    $("#box").load("/abc");
  });
});


