function login_function() {

  var email = document.getElementById('inputEmail').value;
  var password = document.getElementById('inputPassword').value;
  var params = 'email='+email+'&password='+password;

  var xhttp = new XMLHttpRequest();
  xhttp.open('POST', 'login_request', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState === 4 && xhttp.status === 200) {
        var response = xhttp.responseText;
        window.alert(response);
        if (response=="True"){
          window.alert("you have been logged in");
          window.location.replace('../');
        }else{

          window.alert(response)

        }
      } else {
        console.error(xhttp.statusText);
      }
    };
  xhttp.send(params);
  return false;
}
