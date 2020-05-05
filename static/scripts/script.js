document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var private_socket = io.connect('http://127.0.0.1:5000/private')






    document.querySelector('#form').onsubmit = function() {
        private_socket.emit('username',   document.querySelector('#username').value);
        const request = new XMLHttpRequest();
        const username = document.querySelector('#username').value;
        request.open('POST', '/username');
        // Callback function for when request completes
      request.onload = () => {

          // Extract JSON data from request
          const data = JSON.parse(request.responseText);

          // Update the result div
          if (data.success) {

            document.querySelector('h2').innerHTML =  'Hello '+ data.username;
          }
          else {
              document.querySelector('h2').innerHTML = 'Private Chat';
          }
      }      // Add data to send with request
        const data = new FormData();
        data.append('username', username);

        // Send request
        request.send(data);

        return false;
    };


    document.querySelector('#send_private_message').onclick = function() {
        var recipient =   document.querySelector('#send_to_username').value;
        var message_to_send =   document.querySelector('#private_message').value;
        var sender  =  document.querySelector('#username').value


        private_socket.emit('private_message', {'username' : recipient,'sender':sender, 'message' : message_to_send});
        document.querySelector('#private_message').value = '';
        // Autofocus on text box
        document.querySelector("#private_message").focus();
    };

    private_socket.on('new_private_message', function(data) {
        alert(data.sender + '  has send a message to You: ' +data.message);
    });

        // Make 'enter' key submit message
        let message = document.getElementById("private_message");
        message.addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                document.getElementById("send_private_message").click();
            }
        });

});
