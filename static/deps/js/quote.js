$(document).ready(function () {
    toggleNoQuotesPlaceholder();
    $(document).on('submit', '.del-quote-form', function (e) {
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    form.closest('.table-row').remove();
                    showMessage(response.message, true);
                    toggleNoQuotesPlaceholder();
                } else {
                    showMessage('Не удалось удалить цитату.', false);
                }
            },
            error: function () {
                showMessage('Ошибка сервера при попытке удалить цитату.', false);
            }
        });
    });

        $(document).on('submit', '.change-weight-form', function (e) {
        e.preventDefault();
        const form = $(this);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                if (response.success) {
                    showMessage(response.message, true);
                } else {
                    showMessage('Не удалось удалить изменить вес цитаты.', false);
                }
            },
            error: function () {
                showMessage('Ошибка сервера при попытке изменить вес цитаты.', false);
            }
        });
    });


    function toggleNoQuotesPlaceholder() {
        const $tableBody = $('.table-body');
        const hasItems = $tableBody.children('.table-row').length > 0;
        console.log($tableBody.html());
        const $placeHolder = $('#no-quotes-placeholder');
        console.log($placeHolder);
        if (hasItems) {
            $placeHolder.hide();
        } else {
            $placeHolder.css('display', 'table-row');
        }
    }
})