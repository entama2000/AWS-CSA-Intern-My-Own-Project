const form = document.getElementById('loginForm');
const responseContainer = document.createElement('div');
document.body.appendChild(responseContainer);

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const in_email = document.getElementById('email').value;
    const in_password = document.getElementById('password').value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://su7quiromg.execute-api.us-east-1.amazonaws.com/dev/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { email: in_email, password: in_password};

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            const statusCode = response.statusCode;
            const body = JSON.parse(response.body);

            console.log("statusCode-login: " + statusCode);
            
            if (statusCode === 200) {
                const token = response.session_id;
                document.cookie = `token=${token}; path=/`;
                console.log(token);
                window.location.href = 'logedin/success.html';
            } else {
                responseContainer.textContent = body;
                console.log(body);
            }
        }
    };

    xhr.send(JSON.stringify(data));
});