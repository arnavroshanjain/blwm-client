function contact() {

    var first_name = document.getElementById('FirstName').value;
    var Last_name = document.getElementById('LastName').value;
    var email = document.getElementById('Email').value;
    var number = document.getElementById('Numbers').value;
    var comment = document.getElementById('Comments').value;
    

  
    var params = 'first_name='+FirstName+ '&last_name'+LastName+'&email'+Email+'&number'+Numbers+'&comment'+Comments;
  
    var xhttp = new XMLHttpRequest();
  
    xhttp.open('POST', 'login_request', true);
  
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