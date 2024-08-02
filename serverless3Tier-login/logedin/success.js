const messageArea = document.getElementById('messageArea');
// cookieからtokenを取得する関数
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}

// tokenが存在する場合、sessionAPIへリクエストを送信する
const token = getCookie('token');
if (token) {
    console.log(token)
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://su7quiromg.execute-api.us-east-1.amazonaws.com/dev/session', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { token: token };

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            const statusCode = response.statusCode;
            const in_email = response.email

            console.log("statusCode-session: " + statusCode);

            if (statusCode === 200) {
                console.log(in_email);
                document.getElementById('messageArea').innerHTML = "Hello " + in_email;
            } else {
                window.location.href = '../index.html';
            }
            // StatusCodeが200以外の場合ログイン画面へ戻す
        }
    };

    xhr.send(JSON.stringify(data));
}