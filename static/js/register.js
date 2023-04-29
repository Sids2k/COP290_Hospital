  document.getElementById('#register-form').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    // Get form values
    var username = document.getElementById('username-input').value;
    var password = document.getElementById('password-input').value;
    var name = document.getElementById('name-input').value;
    var age = document.getElementById('age-input').value;
    var role = [];
    var roleInputs = document.querySelectorAll('input[name="role"]:checked');
    roleInputs.forEach(function(input) {
      role.push(input.value);
    });
    var gender = document.querySelector('input[name="gender"]:checked').value;

    // Create an object to hold the form data
    var formData = {
      username: username,
      password: password,
      name: name,
      age: age,
      role: role,
      gender: gender
    };

    // You can perform any necessary validation here before sending the form data to the server

    // Send the form data to the server (replace the URL with your server-side endpoint)
    fetch('register', {
      method: 'POST',
      body: JSON.stringify(formData),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function(response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error: ' + response.status);
      }
    })
    .then(function(data) {
      // Handle successful registration response
      console.log('Registration successful:', data);
      // You can redirect to another page or show a success message here
    })
    .catch(function(error) {
      // Handle error response
      console.error('Registration error:', error);
      // You can show an error message here
    });
  });