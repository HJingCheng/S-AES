$(document).ready(function () {
    let pairs = []; // 存储明密文对的列表

    // 添加对按钮点击事件
    $("#addPairBtn").click(function () {
        const plaintext = $(".plaintext").val();
        const ciphertext = $(".ciphertext").val();

        if (plaintext && ciphertext) {
            pairs.push({plaintext: plaintext, ciphertext: ciphertext});

            // 将对添加到前端的卡片中
            $("#pairsList").append(`<li class="list-group-item">明文: ${plaintext}, 密文: ${ciphertext}</li>`);

            // 清空输入框
            $(".plaintext").val("");
            $(".ciphertext").val("");
        } else {
            // 更新toast的内容
            $('#toastBody').text('明文或密文输入为空，请输入有效的明文和密文！');
            // 显示toast
            $('#emptyToast').toast('show');
        }
    });

    // 进行破解按钮点击事件
    $(".forceBtn").click(function () {
        if (pairs.length === 0) {
            // 更新toast的内容
            $('#toastBody').text('请添加明密文对！');
            // 显示toast
            $('#emptyToast').toast('show');
            return;
        }
        $.ajax({
            url: '/api/crack',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({"pairs": pairs}),
            success: function (response) {
                console.log(response);
                $("#crackResult").empty();  // 清除之前的结果

                if (response.status === "success") {
                    let keyPairs = response.result.keys;
                    if (keyPairs.length > 0) {
                        for (let i = 0; i < keyPairs.length; i++) {
                            let formattedString = `Key1: ${keyPairs[i].key1}, Key2: ${keyPairs[i].key2}`;
                            // 在界面上显示结果
                            $("#crackResult").append('<li class="list-group-item">' + formattedString + '</li>');
                        }
                    } else {
                        $("#crackResult").append('<li class="list-group-item">没有找到匹配的密钥对。</li>');
                    }
                } else {
                    // 显示错误信息或其他提示信息
                    $("#crackResult").append('<li class="list-group-item">' + response.message + '</li>');
                }

                // 显示用时
                $("#timeTaken").text(`所用时间：${response.result.timeTaken.toFixed(2)}秒`);
            },
            error: function (error) {
                console.log(error);
                // 显示一些错误信息，告知用户请求失败
                $("#crackResult").append('<li class="list-group-item">请求失败，请重试。</li>');
            }
        });
    });
});
