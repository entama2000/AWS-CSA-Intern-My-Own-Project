// URLからクエリ文字列を抽出する関数
function getQueryString(key) {
    // const queryString = window.location.search;
    // const urlParams = new URLSearchParams(queryString);
    // return urlParams.get(key);
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    return params.get(key);
}
  
// IdTokenの値を取得する
const token = getQueryString('id_token');
const form = document.getElementById('loginForm');

const messageArea = document.getElementById('messageArea');

if (token) {
    document.cookie = `token=${token}; path=/`;
    console.log(token);
    window.location.href = './success.html';
} else {
    window.location.href = '../index.html';
}