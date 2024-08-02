const form = document.getElementById('loginForm');
const responseContainer = document.createElement('div');
document.body.appendChild(responseContainer);

// URLからクエリ文字列を抽出する関数
function getQueryParam(name) {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  return urlParams.get(name);
}

const in_id = getQueryParam('id');
if (!in_id) {
    window.location.href = '../index.html';
}
console.log(in_id);

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const in_otp = document.getElementById('otp').value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://rqe0g3nujg.execute-api.us-east-1.amazonaws.com/dev/login-2fa-checker', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { id: in_id, otp: in_otp };

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            const statusCode = response.statusCode;
            //const body = JSON.parse(response.body);

            console.log("statusCode-login: " + statusCode);
            
            if (statusCode === 200) {
                const answer = JSON.parse(response.body);

                const token = answer.IdToken;

                document.cookie = `token=${token}; path=/`;
                console.log(token);
                window.location.href = '../logedin/success.html';

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