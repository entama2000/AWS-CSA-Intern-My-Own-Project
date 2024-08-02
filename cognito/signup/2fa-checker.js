const form = document.getElementById('loginForm');
const responseContainer = document.createElement('div');
document.body.appendChild(responseContainer);

// URLからクエリ文字列を抽出する関数
function getQueryParam(name) {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  return urlParams.get(name);
}

const in_email = getQueryParam('email');
if (!in_email) {
    window.location.href = '../index.html';
}
console.log(in_email);

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const in_otp = document.getElementById('otp').value;
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;
    
    if (password1 == password2) {
        //do nothing
    } else {
        responseContainer.textContent = "Passwords do not match";
        return;
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://rqe0g3nujg.execute-api.us-east-1.amazonaws.com/dev/signup', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { id: in_email, password: password1, otp: in_otp };

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            const statusCode = response.statusCode;
            //const body = JSON.parse(response.body);

            console.log("statusCode-login: " + statusCode);
            
            if (statusCode === 200) {
                const answer = JSON.parse(response.body);
                window.location.href = './done.html';

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