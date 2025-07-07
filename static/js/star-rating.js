
document.addEventListener('DOMContentLoaded', function() {
    const starRatingContainer = document.querySelector('.star-rating');
    
    if (!starRatingContainer) {
        return; 
    }

    const ratingInput = document.getElementById('rating-value');
    const stars = starRatingContainer.querySelectorAll('.star');

    function updateStars(rating) {
        stars.forEach(star => {
            if (star.getAttribute('data-value') <= rating) {
                star.style.color = '#ffc107';
            } else {
                star.style.color = '#555';
            }
        });
    }

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            ratingInput.value = value;
            starRatingContainer.setAttribute('data-rating', value);
            updateStars(value);
        });
    });

    starRatingContainer.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('star')) {
            updateStars(e.target.getAttribute('data-value'));
        }
    });

    starRatingContainer.addEventListener('mouseout', () => {
        const currentRating = starRatingContainer.getAttribute('data-rating');
        updateStars(currentRating || 0);
    });
});