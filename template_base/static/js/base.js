document.addEventListener('DOMContentLoaded', () => {

    const messages = document.querySelectorAll('.message');

    messages.forEach((message) => {
        setTimeout(() => {
            message.classList.add('hide');

            setTimeout(() => {
                message.remove();
            }, 500);

        }, 5000);
    });

});