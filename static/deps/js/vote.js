$(document).ready(function () {
    $(document).on('submit', '.vote-form', function (e) {
        e.preventDefault();
        const $form = $(this);
        const quote_card = $form.closest('.quote-card');
        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    const $newItem = $(response.item_html);
                    quote_card.replaceWith($newItem);
                }
                 return showMessage(response.message, response.success);

            },
            error: function (xhr, status, err) {
                console.error('vote error', status, err, xhr.responseText);
                return showMessage('Ошибка сервера при попытке проголосовать.', false);
            }
        });
    });

});