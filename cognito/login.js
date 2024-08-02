const form = document.getElementById('loginForm');
const responseContainer = document.createElement('div');
document.body.appendChild(responseContainer);

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const in_id = document.getElementById('inid').value;
    const in_password = document.getElementById('password').value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://rqe0g3nujg.execute-api.us-east-1.amazonaws.com/dev/login-2fa', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { id: in_id, password: in_password};

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            const statusCode = response.statusCode;
            //const body = JSON.parse(response.body);

            console.log("statusCode-login: " + statusCode);
            
            if (statusCode === 200) {
                const answer = JSON.parse(response.body);

                // const token = answer.IdToken;

                // document.cookie = `token=${token}; path=/`;
                // console.log(token);
                window.location.href = '2fa/2fa-checker.html?id='+in_id;

                responseContainer.textContent = "Loged in Successfully";
            } else {
                const answer = JSON.parse(response.body);
                console.log(answer.message);
                responseContainer.textContent = answer.message;
            }
        }
    };

    xhr.send(JSON.stringify(data));
});