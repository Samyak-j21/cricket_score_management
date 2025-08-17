document.addEventListener('DOMContentLoaded', function () {
    // Simulate live score updates
    const liveButtons = document.querySelectorAll('.live-update-btn');
    liveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const matchId = button.dataset.matchId;
            const scoreDisplay = document.querySelector(`#score-${matchId}`);
            if (scoreDisplay) {
                // Simulate score update (replace with WebSocket in production)
                const currentScore = parseInt(scoreDisplay.textContent) || 0;
                scoreDisplay.textContent = currentScore + Math.floor(Math.random() * 6);
                scoreDisplay.classList.add('score-updated');
                setTimeout(() => scoreDisplay.classList.remove('score-updated'), 500);
            }
        });
    });

    // Smooth scroll for navigation
    document.querySelectorAll('a.nav-link').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            document.querySelector(targetId).scrollIntoView({ behavior: 'smooth' });
        });
    });
});