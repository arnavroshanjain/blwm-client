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
      if (response == 'true') {
        window.alert('Account created')
        window.location.replace('../register/user_select');
      } else {
        window.alert(response)
      }
    } else {
      console.error(xhttp.statusText);
    }
  };
  xhttp.send(params);
  return false;
  }

function contact() {
    var first_name = document.getElementById('first_name').value;
    var last_name = document.getElementById('last_name').value;
    var email = document.getElementById('email').value;
    var number = document.getElementById('number').value;
    var comment = document.getElementById('comment').value;
    var params = 'first_name='+first_name+'&last_name='+last_name+'&email='+email+'&number='+number+'&comment='+comment;
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', 'contact_request', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
          var response = xhttp.responseText;
          if (response == 'True') {
            window.location.replace('../');
          } else {
            window.alert(response)
          }
        } else {
          console.error(xhttp.statusText);
        }
      };
    xhttp.send(params);
    return false;
  }

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
        if (response=="True"){
          window.alert("you have been logged in");
          window.location.replace('../');
        } else if (response=="register partially complete") {
          window.alert("you have been logged in");
          window.location.replace('../register/user_select');
        }else{
          window.alert(response);
        }
      } else {
        console.error(xhttp.statusText);
      }
    };
  xhttp.send(params);
  return false;
}

function update_logo() {
  var photo = document.getElementById('pfp-select').files[0];
  if (photo['type'].split('/')[0] !== 'image') {
    window.alert('Invalid file type, please select an image')
    return 'Invalid file type'
  }
  const reader = new FileReader();
  reader.addEventListener("load", () => {

    document.getElementById('pfp-select-label').classList.remove("btn-secondary");
    document.getElementById('pfp-select-label').classList.add("pfp-select-label");
    document.getElementById('pfp-select-label').innerHTML = '';
    document.getElementById('pfp-select-label').style.backgroundImage = `url(${reader.result})`;
  });
  photo_url = reader.readAsDataURL(photo);
}

function create_school_request() {
  var name = document.getElementById('school_name').value;
  var address = document.getElementById('school_address').value;
  var email = document.getElementById('school_email').value;
  var phone_number = document.getElementById('school_phone_number').value;
  var website = document.getElementById('school_website').value;
  var params = 'name='+name+'&address='+address+'&email='+email+'&phone_number='+phone_number+'&website='+website;
  var xhttp = new XMLHttpRequest();
  xhttp.open('POST', 'school_request', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState === 4 && xhttp.status === 200) {
        var response = xhttp.responseText;
        if (response == 'True') {
          window.alert('School creation successful')
          window.location.replace('../');
        } else {
          window.alert(response);
        }
      } else {
        console.error(xhttp.statusText);
      }
    };
  xhttp.send(params);
  return false;
}


function update_profile(){
  var firstName = document.getElementById('inputFName').value;
  var lastName = document.getElementById('inputLName').value;
  var userId = document.getElementById('userID').value;
  // var userId = document.getElementById('userID').value;
  var email = document.getElementById('inputEmail').value;
  console.log(firstName, lastName, userId, email);
  var params = 'inputFName='+firstName+'&inputLName='+lastName+'&inputEmail='+email+'&userId='+userId;
  console.log(firstName, lastName, email);
  var params = 'inputFName='+firstName+'&inputLName='+lastName+'&inputEmail='+email;
  var xhttp = new XMLHttpRequest();
  xhttp.open('POST', 'update', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState === 4 && xhttp.status === 200) {
        var response = xhttp.responseText;
        window.alert(response);
        if (response=="True"){
        if (response=="true"){
          window.alert("Information has been Updated");
          window.location.replace('/user');
          var userId = document.getElementById('user_id').value;
          window.location.replace('/user/'+userId);
        }else{

          window.alert(response)

        }
      }else {
        console.error(xhttp.statusText);
      }
    };
  xhttp.send(params);
  return false;
}
