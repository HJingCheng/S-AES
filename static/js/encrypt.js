$("#encryptBtn").click(function () {
    callApi("encrypt");
});

$("#decryptBtn").click(function () {
    callApi("decrypt");
});

function callApi(method) {
    var encryptionType = $("input[name='encryptionType']:checked").val();
    var key = $("#keyInput").val();
    var text = $("#textInput").val();

    var apiUrl = "/api/" + method;
    var requestData = {};

    if (key === "") {
        // 更新toast的内容
        $('#toastBody').text('密钥输入为空，请输入有效的密钥！');
        // 显示toast
        $('#emptyToast').toast('show');
        return;
    }

    if (text === "") {
        // 更新toast的内容
        $('#toastBody').text('文本输入为空，请输入有效的文本！');
        // 显示toast
        $('#emptyToast').toast('show');
        return;
    }

    if (encryptionType === "ascii" && method === "encrypt") {
        apiUrl = "/api/encrypt_string";
        requestData = {
            "input_str": text,
            "key": key
        };
    } else if (encryptionType === "ascii" && method === "decrypt") {
        apiUrl = "/api/decrypt_string";
        requestData = {
            "encrypted_base64_str": text,
            "key": key
        };
    } else {
        requestData = {
            "plaintext": text,
            "key": key
        };
        if (method === "decrypt") {
            requestData = {
                "ciphertext": text,
                "key": key
            };
        }
    }

    if (encryptionType === "ascii" && method === "encrypt") {
        apiUrl = "/api/encrypt_string";
    } else if (encryptionType === "ascii" && method === "decrypt") {
        apiUrl = "/api/decrypt_string";
    } else if (encryptionType === "double" && method === "encrypt") {
        apiUrl = "/api/double_encrypt";
    } else if (encryptionType === "double" && method === "decrypt") {
        apiUrl = "/api/double_decrypt";
    } else if (encryptionType === "tri" && method === "encrypt") {
        apiUrl = "/api/tri_encrypt";
    } else if (encryptionType === "tri" && method === "decrypt") {
        apiUrl = "/api/tri_decrypt";
    }

    $.ajax({
        url: apiUrl,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (response) {
            if (method === "encrypt") {
                $("#outputText").text(response.ciphertext || response.encrypted_base64_str || response.double_ciphertext || response.tri_ciphertext);
            } else {
                $("#outputText").text(response.plaintext || response.output_str || response.double_plaintext || response.tri_plaintext);
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}
