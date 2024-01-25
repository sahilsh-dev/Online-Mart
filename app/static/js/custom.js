// Quick View Modal

const quickviewModal = document.getElementById('modalQuickview');
const largeImageContainer = document.querySelector('.product-large-image .swiper-wrapper');
const thumbnailImageContainer = document.querySelector('.product-image-thumb .swiper-wrapper');

function replaceImages(imagePaths) {
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


// Search Modal

const searchInput = document.querySelector('#search input');
const searchItemsContainer = document.querySelectorAll('#search-items li');

const debounce = (func, timeout=300) => {
    let timer;
    searchItemsContainer.forEach(item => item.style.display = 'none');
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

const updateResults = () => {
    const searchQuery = searchInput.value;
    fetch(`/shop/search?search_term=${searchQuery}`)
        .then(response => response.json())
        .then(data => {
            searchItemsContainer.forEach(item => item.style.display = 'none');
            data.forEach((item, i) => {
                const heading = searchItemsContainer[i].querySelector('h2');
                const link = searchItemsContainer[i].querySelector('a');
                heading.innerText = item.title;
                link.href = item.url;

                searchItemsContainer[i].style.display = 'block';
            })
        })
        .catch(error => console.warn('Error fetching search results:', error));
}

const updateSearchResults = debounce(() => updateResults());


// Show Address Form

const editAddressBtn = document.querySelector('#address .view');
if (editAddressBtn) {
    editAddressBtn.addEventListener('click', () => {
        const addressForm = document.querySelector('#address-form');
        addressForm.style.display = 'block';
    })
}
