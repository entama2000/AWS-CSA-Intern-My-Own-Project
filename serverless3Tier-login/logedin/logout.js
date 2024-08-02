// ログアウトボタンの参照を取得
const logoutBtn = document.getElementById('logoutBtn');

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}

// ログアウトボタンのクリックイベントハンドラを設定
logoutBtn.addEventListener('click', () => {

    // document.cookie = "token=; max-age=0";
    
    // tokenが存在する場合、logoutAPIへリクエストを送信する
　  const token = getCookie('token');
  
    if (token) {
        console.log(token)
        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://su7quiromg.execute-api.us-east-1.amazonaws.com/dev/session/logout', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
    
        const data = { token: token };
    
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                const response = JSON.parse(xhr.responseText);
                const statusCode = response.statusCode;
                const in_email = response.email;
                const in_body = response.body;
    
                console.log("statusCode-logout: " + statusCode);
    
                if (statusCode === 200) {
                    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                    console.log("logout-email: " + in_email);
                    window.location.href = '../index.html';
                } else {
                    document.getElementById('messageArea').innerHTML = "Who are you??: " + in_body;
                }
            }
        };
    
        xhr.send(JSON.stringify(data));
    }
});