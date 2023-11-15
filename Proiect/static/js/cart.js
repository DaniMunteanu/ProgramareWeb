increaseButtons.forEach((button, index) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentSticker = event.target.closest(".cart-sticker");
        const quantityElement = currentSticker.querySelector(".sticker-quantity");
        const priceElement = currentSticker.querySelector(".cart-sticker-price");
        const pricePerSticker = parseFloat(priceElement.getAttribute("data-price"));
        const currentQuantity = parseInt(quantityElement.textContent);

        quantityElement.textContent = currentQuantity + 1;
        updateCartItemPrice(priceElement, pricePerSticker, currentQuantity + 1);
    });
});

decreaseButtons.forEach((button, index) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentSticker = event.target.closest(".cart-sticker");
        const quantityElement = currentSticker.querySelector(".sticker-quantity");
        const priceElement = currentSticker.querySelector(".cart-sticker-price");
        const pricePerSticker = parseFloat(priceElement.getAttribute("data-price"));
        const currentQuantity = parseInt(quantityElement.textContent);

        if (currentQuantity > 1) {
            quantityElement.textContent = currentQuantity - 1;
            updateCartItemPrice(priceElement, pricePerSticker, currentQuantity - 1);
        }
    });
});

function updateCartItemPrice(priceElement, pricePerSticker, quantity) {
    const totalPrice = (pricePerSticker * quantity).toFixed(2);
    priceElement.textContent = "$" + totalPrice;
}
function updateCartCount() {
    var cartCount = document.querySelector('.cart-count');
    fetch("http://127.0.0.1:8000/fetch-cart-count/")
        .then(response => response.json())
        .then(data => {
            cartCount.textContent = data.cart_count;
        });
}

updateCartCount();


