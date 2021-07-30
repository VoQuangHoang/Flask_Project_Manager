$(document).ready(function () {
    $.validator.addMethod("greaterThan",
        function (value, element, params) {
            if (!/Invalid|NaN/.test(new Date(value))) {
                return new Date(value) > new Date($(params).val());
            }
            return isNaN(value) && isNaN($(params).val()) ||
                (Number(value) > Number($(params).val()));
        }, '「失効日」は「交付年月日」より未来の日で入力してください。');

    $.validator.addMethod('valid_name_kana', function (value) {
        if (value === '') {
            return true
        }
        var regex = /^([ァ-ン]|ー)+$/;
        return value.match(regex);
    }, 'ER009: 「カタカナ氏名」をカタカナで入力してください');
    $.validator.addMethod('valid_persional_email', function (value) {
        if (value === '') {
            return true
        }
        var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/
        return value.match(regex);
    }, '「アカウント名」をyouremail@example.com形式で入力してください');

    $("#addForm").validate({
        // onfocusout: false,
        // onkeyup: false,
        // onclick: false,
        rules: {
            "full_name_kana": {
                valid_name_kana: true
            },
            "persional_email": {
                valid_persional_email: true
            },
        },
        messages: {
            "email": {
                required: "「アカウント名」を入力してください"
            },
            "role": {
                required: "「ロール」を入力してください"
            },
            "group": {
                required: "「グループ」を入力してください"
            },
            "full_name": {
                required: "「氏名」を入力してください"
            },
            "birthday": {
                required: "「生年月日」を入力してください"
            },
            "tel": {
                required: "「電話番号」を入力してください"
            },
            "password": {
                required: "「パスワード」を入力してください"
            },
            "confirm": {
                required: "「パスワード（確認）」を入力してください"
            },

        },
        onkeyup: function (element) {
            $(element).valid();
        },
        onclick: function (element) {
            $(element).valid();
        },
        onfocusout: function (element) {
            $(element).valid();
        },
        errorClass: 'badge badge-danger error',
        errorElement: 'label',
        highlight: function (element, errorClass, validClass) {
            $(element).closest('.validate').addClass(errorClass).removeClass(validClass);
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).closest('.validate').addClass(validClass).removeClass(errorClass);
        },

    });
})