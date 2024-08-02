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

            console.log("statusCode-session: " + statusCode);

            if (statusCode === 200) {
                // 別のページにリダイレクト
                window.location.href = 'logedin/success.html';
            }
            // StatusCodeが200以外の場合は何もしない
        }
    };

    xhr.send(JSON.stringify(data));
}