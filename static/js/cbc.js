$(document).ready(function() {

    // CBC加密
    $("#encryptCBCBtn").click(function() {
        let longtext = $("#longTextInput").val();
        let key = $("#CBCkey").val();
        let IV = $("#ivInput").val();
        if (longtext === "") {
            // 更新toast的内容
            $('#toastBody').text('明文输入为空，请输入有效的明文！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        if (key === "") {
            // 更新toast的内容
            $('#toastBody').text('密钥输入为空，请输入有效的密钥！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        if (IV === "") {
            // 更新toast的内容
            $('#toastBody').text('IV输入为空，请输入有效的IV！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        $.ajax({
            url: '/api/cbc/encrypt',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "longtext": longtext,
                "key": key,
                "IV": IV
            }),
            success: function(response) {
                $("#cipherTextEdit").val(response.encrypted);
                $("#CBCoutputText").text("加密结果: " + response.encrypted);
            },
            error: function(error) {
                console.log(error);
                $("#CBCoutputText").text("加密失败: " + error.statusText);
            }
        });
    });

    // CBC解密
    $("#decryptCBCBtn").click(function() {
        let longcipher = $("#cipherTextEdit").val();
        let key = $("#CBCkey").val();
        let IV = $("#ivInput").val();
        if (longcipher === "") {
            // 更新toast的内容
            $('#toastBody').text('密文输入为空，请输入有效的密文或者加密！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        if (key === "") {
            // 更新toast的内容
            $('#toastBody').text('密钥输入为空，请输入有效的密钥！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        if (IV === "") {
            // 更新toast的内容
            $('#toastBody').text('IV输入为空，请输入有效的IV！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        $.ajax({
            url: '/api/cbc/decrypt',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "longcipher": longcipher,
                "key": key,
                "IV": IV
            }),
            success: function(response) {
                $("#CBCoutputText").text("解密结果: " + response.decrypted);
            },
            error: function(error) {
                console.log(error);
                $("#CBCoutputText").text("解密失败: " + error.statusText);
            }
        });
    });
});
