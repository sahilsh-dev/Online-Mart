// const quickviewModal = document.getElementById('modalQuickview');

// function recreateImages(imagePaths) {
//     const largeImageContainer = document.querySelector('.product-large-image>.swiper-wrapper');
//     const thumbnailImageContainer = document.querySelector('.product-image-thumb .swiper-wrapper');

//     const width = thumbnailImageContainer.querySelector('.product-image-thumb-single').offsetWidth;

//     // Clear existing images
//     largeImageContainer.innerHTML = '';
//     thumbnailImageContainer.innerHTML = '';
//     // Create and append new images
//     imagePaths.forEach((imagePath, index) => {
//         // Create large image
//         const largeImage = document.createElement('div');
//         largeImage.className = 'product-image-large-image swiper-slide img-responsive';
//         largeImage.innerHTML = `<img src="${imagePath}" alt="Image ${index + 1}">`;
//         largeImageContainer.appendChild(largeImage);

//         // Create thumbnail image
//         const thumbnailImage = document.createElement('div');
//         thumbnailImage.className = 'product-image-thumb-single swiper-slide swiper-slide-visible swiper-slide-next';
//         thumbnailImage.innerHTML = `<img class="img-fluid" src="${imagePath}" alt="Thumbnail ${index + 1}">`;
//         thumbnailImage.style.width = `${width}px`;
//         thumbnailImage.style.marginRight = '10px';
//         thumbnailImageContainer.appendChild(thumbnailImage);
//     });
// }


// quickviewModal.addEventListener('show.bs.modal', function (event) {
//     const quickviewBtn = event.relatedTarget;
//     const productId = quickviewBtn.getAttribute('data-bs-product-id');

//     const productDataURL = `/product/${productId}`;
//     fetch(productDataURL)
//         .then(response => response.json())
//         .then(data => {
//             quickviewModal.querySelector('.product-details-text .title').innerText = data.title;
//             quickviewModal.querySelector('.product-details-text .price').innerText = `₹${data.price}`;
//             quickviewModal.querySelector('.modal-product-about-text p').innerText = data.description;
//             recreateImages(data.images);
//         });
// })


const quickviewModal = document.getElementById('modalQuickview');
const largeImageContainer = document.querySelector('.product-large-image>.swiper-wrapper');
const thumbnailImageContainer = document.querySelector('.product-image-thumb .swiper-wrapper');

function recreateImages(imagePaths) {
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
            recreateImages(data.images);
        })
        .catch(error => console.error('Error fetching product data:', error));
});
