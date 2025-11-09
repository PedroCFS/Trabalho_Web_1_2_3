document.addEventListener('DOMContentLoaded', function() {
    const logo = document.querySelector('.logo');
    const homeBtn = document.getElementById('home-btn');
    const menuBtn = document.getElementById('menu-btn');
    const gamesBtn = document.getElementById('games-btn');

    if (logo) {
        logo.addEventListener('click', () => {
            window.location.href = '/';
        });
    }

    if (homeBtn) {
        homeBtn.addEventListener('click', () => {
            window.location.href = '/';
        });
    }

    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            window.location.href = '/cardapio/';
        });
    }

    if (gamesBtn) {
        gamesBtn.addEventListener('click', () => {
            window.location.href = '/jogos/';
        });
    }
});

