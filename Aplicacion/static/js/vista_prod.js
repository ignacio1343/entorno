document.getElementById('increaseQuantity').addEventListener('click', function () {
    var quantityInput = document.getElementById('quantity');
    var quantity = parseInt(quantityInput.value);
    quantityInput.value = quantity + 1;
});

document.getElementById('decreaseQuantity').addEventListener('click', function () {
    var quantityInput = document.getElementById('quantity');
    var quantity = parseInt(quantityInput.value);
    if (quantity > 1) {
        quantityInput.value = quantity - 1;
    }
});

document.getElementById('addToCartBtn').addEventListener('click', function () {
    var quantity = parseInt(document.getElementById('quantity').value);
    alert('Agregado ' + quantity + ' al carrito.');
    // Aquí puedes agregar la lógica para agregar el producto al carrito
});