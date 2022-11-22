



function send_register(){
  var name = document.getElementById('name').value;
  var lastName = document.getElementById('lastName').value;
  var email = document.getElementById('email').value;
  var password = document.getElementById('password').value;

  var params = 'name='+name+'&lastName='+lastName+'&email='+email+'&password='+password;
  var xhttp = new XMLHttpRequest();
  xhttp.open('POST', 'register_request', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      var response = xhttp.responseText;
      if (response == 'True') {
        window.location.replace('../');
      } else {
        document.getElementById('error_output').innerHTML = response;
      }
    } else {
      console.error(xhttp.statusText);
    }
  };
  xhttp.send(params);
  return false;
  }
