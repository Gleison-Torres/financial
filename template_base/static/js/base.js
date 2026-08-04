document.addEventListener('DOMContentLoaded', () => {

    const message = document.getElementById('message');

    if (message) {
        setTimeout(() => {
            message.classList.add('hide');

            setTimeout(() => {
                message.remove();
            }, 500); // espera a animação terminar
        }, 5000);
    }

});