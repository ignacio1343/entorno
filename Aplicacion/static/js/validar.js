

const stockInput = document.getElementById('stock');
const valorInput = document.getElementById('valor');

// Agrega event listeners para el evento "input" en cada campo
stockInput.addEventListener('input', function() {
    // Si el valor es negativo, establece el valor como 0
    if (this.value < 0) {
        this.value = 0;
    }
});

valorInput.addEventListener('input', function() {
    // Si el valor es negativo, establece el valor como 0
    if (this.value < 0) {
        this.value = 0;
    }
});
