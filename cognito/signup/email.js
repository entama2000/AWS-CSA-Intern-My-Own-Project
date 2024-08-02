const form = document.getElementById('loginForm');
const responseContainer = document.createElement('div');
document.body.appendChild(responseContainer);

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const in_email = document.getElementById('email').value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://rqe0g3nujg.execute-api.us-east-1.amazonaws.com/dev/signup-2fa', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { email: in_email };

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            const statusCode = response.statusCode;
            //const body = JSON.parse(response.body);

            console.log("statusCode-login: " + statusCode);
            
            if (statusCode === 200) {
                const answer = JSON.parse(response.body);

                window.location.href = './2fa-checker.html?email=' + in_email;

                responseContainer.textContent = answer.message;
            } else {
                const answer = JSON.parse(response.body);
                console.log(answer.message);
                responseContainer.textContent = answer.message;
            }
        }
    };

    xhr.send(JSON.stringify(data));
});