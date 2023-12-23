const quickviewModal = document.getElementById('modalQuickview');
const largeImageContainer = document.querySelector('.product-large-image .swiper-wrapper');
const thumbnailImageContainer = document.querySelector('.product-image-thumb .swiper-wrapper');

function replaceImages(imagePaths) {
    // Hide all existing images
    const allImages = document.querySelectorAll('.product-image-large-image img, .product-image-thumb-single img');
    allImages.forEach(image => image.style.display = 'none');

    // Update image sources based on the data from the backend
    imagePaths.forEach((imagePath, index) => {
        const largeImage = largeImageContainer.children[index].querySelector('img');
        const thumbnailImage = thumbnailImageContainer.children[index].querySelector('img');

        largeImage.src = imagePath;
        thumbnailImage.src = imagePath;

        // Show the images
        largeImage.style.display = 'block';
        thumbnailImage.style.display = 'block';
    });
}

quickviewModal.addEventListener('show.bs.modal', function (event) {
    const quickviewBtn = event.relatedTarget;
    const productId = quickviewBtn.getAttribute('data-bs-product-id');

    const productDataURL = `/product/${productId}`;
    fetch(productDataURL)
        .then(response => response.json())
        .then(data => {
            quickviewModal.querySelector('.product-details-text .title').innerText = data.title;
            quickviewModal.querySelector('.product-details-text .price').innerText = `₹${data.price}`;
            quickviewModal.querySelector('.modal-product-about-text p').innerText = data.description;
            replaceImages(data.images);
        })
        .catch(error => console.error('Error fetching product data:', error));
});
