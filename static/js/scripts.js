function create_school_request() {

    var name = document.getElementById('school_name').value;
    var address = document.getElementById('school_address').value;
    var email = document.getElementById('school_email').value;
    var phone_number = document.getElementById('school_phone_number').value;
    var logo = document.getElementById('school_logo').value;
    var website = document.getElementById('school_website').value;
    var params = 'name='+name+'&address='+address+'&email='+email+'&phone_number='+phone_number+'&logo='+logo+'&website='+website;

    window.alert(params);
    
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', 'school_request', true);
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