(function () {
        var toggle = document.querySelector('[data-nav-toggle]');
        var links = document.getElementById('nav-links');
        if (!toggle || !links) return;
        toggle.addEventListener('click', function () {
            var open = links.classList.toggle('is-open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            toggle.innerHTML = open
                ? '<i class="fa-solid fa-xmark"></i>'
                : '<i class="fa-solid fa-bars"></i>';
        });
    })();