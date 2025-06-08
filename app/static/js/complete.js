// グループ名を取得
console.log(GROUP_NAME);

// nextボタンの処理
document.getElementById('next-button').addEventListener('click', function() {

    // URLを生成
    const nextUrl = this.getAttribute('data-next-url');
    const url = `${nextUrl}?group_name=${encodeURIComponent(GROUP_NAME)}`;

    // ページ遷移
    window.location.href = url;
});

// saveボタンの処理
document.getElementById('save-button').addEventListener('click', function() {
    // 画像のURLを取得
    const imageUrl = document.getElementById('profile-image').src;
    
    // 画像をダウンロードするためのリンクを作成
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = 'profile-image.png';  // ダウンロードするファイル名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
    