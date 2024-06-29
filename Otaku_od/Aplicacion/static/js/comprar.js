function validarCVV(input) {
    // Eliminar cualquier carácter que no sea un número
    input.value = input.value.replace(/\D/g, '');

    // Limitar la longitud del campo a 3 dígitos
    if (input.value.length > 3) {
        input.value = input.value.slice(0, 3);
    }
}

function validarNumeroTarjeta(input) {
    // Eliminar cualquier carácter que no sea un número
    input.value = input.value.replace(/\D/g, '');

    // Limitar la longitud del campo a 16 dígitos
    if (input.value.length > 16) {
        input.value = input.value.slice(0, 16);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const expirationDateInput = document.getElementById("expirationDate");

    expirationDateInput.addEventListener("input", function (event) {
        let input = event.target;
        let value = input.value.replace(/\D/g, ''); // Eliminar cualquier carácter que no sea un número
        let formattedValue = "";

        // Agregar "/" después de los primeros dos caracteres si hay más de dos caracteres
        if (value.length > 2) {
            formattedValue = value.substring(0, 2) + "/" + value.substring(2);
        } else {
            formattedValue = value;
        }

        // Limitar la longitud del campo a 5 caracteres (incluyendo el "/")
        if (formattedValue.length > 5) {
            formattedValue = formattedValue.slice(0, 5);
        }

        input.value = formattedValue;
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var phoneInput = document.getElementById("phone");

    phoneInput.addEventListener("input", function (event) {
        var inputValue = event.target.value;

        // Eliminar caracteres no permitidos, manteniendo solo números y el símbolo "+"
        var cleanInput = inputValue.replace(/[^\d+]/g, "");

        // Limitar la longitud a 12 caracteres (incluido el símbolo "+")
        cleanInput = cleanInput.slice(0, 13);

        // Actualizar el valor del campo de entrada
        phoneInput.value = cleanInput;
    });
});


function validarRut(rut) {
    rut = rut.replace(".", "").replace("-", "");
    var dv = rut.slice(-1).toUpperCase();
    var rut = rut.slice(0, -1);
    if (/^[0-9]+$/g.test(rut)) {
        var suma = 0;
        var mul = 2;
        for (var i = rut.length - 1; i >= 0; i--) {
            suma += rut.charAt(i) * mul;
            if (mul === 7) mul = 2;
            else mul++;
        }
        var res = suma % 11;
        var dvr = 11 - res;
        if (dvr === 11) dvr = 0;
        if (dvr === 10) dvr = "K";
        if (dvr.toString() === dv) {
            return true;
        }
    }
    return false;
}

document.getElementById("idrut").addEventListener("input", function () {
    var rutInput = this.value.trim();
    if (validarRut(rutInput)) {
        this.setCustomValidity('');
    } else {
        this.setCustomValidity('Ingrese rut sin punto y con guión');
    }
});

function redirectToHash() {
    window.location.href = "index.html";
}

//metodo de pago bonito

function showPaymentFields() {
    var select = document.getElementById("metodo_pago");
    var paymentFields = document.getElementById("paymentFields");
    if (select.value !== "") {
        paymentFields.style.display = "block";
    } else {
        paymentFields.style.display = "none";
    }
}

//Validacion rut

function checkRut(rut) {
    // Despejar Puntos
    var valor = rut.value.replace('.', '');
    // Despejar Guión
    valor = valor.replace('-', '');

    // Aislar Cuerpo y Dígito Verificador
    cuerpo = valor.slice(0, -1);
    dv = valor.slice(-1).toUpperCase();

    // Formatear RUN
    rut.value = cuerpo + '-' + dv

    // Si no cumple con el mínimo ej. (n.nnn.nnn)
    if (cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false; }

    // Calcular Dígito Verificador
    suma = 0;
    multiplo = 2;

    // Para cada dígito del Cuerpo
    for (i = 1; i <= cuerpo.length; i++) {
        // Obtener su Producto con el Múltiplo Correspondiente
        index = multiplo * valor.charAt(cuerpo.length - i);
        // Sumar al Contador General
        suma = suma + index;
        // Consolidar Múltiplo dentro del rango [2,7]
        if (multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
    }
    // Calcular Dígito Verificador en base al Módulo 11
    dvEsperado = 11 - (suma % 11);
    // Casos Especiales (0 y K)
    dv = (dv == 'K') ? 10 : dv;
    dv = (dv == 11) ? 0 : dv;
    // Validar que el Cuerpo coincide con su Dígito Verificador
    if (dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }
    // Si todo sale bien, eliminar errores (decretar que es válido)
    rut.setCustomValidity('');
}

//Info de la compra

// Obtener referencia al elemento del botón y al div con los detalles de la compra
const toggleCartButton = document.getElementById('toggleCart');
const detallesCompra = document.getElementById('detallesCompra');

// Agregar evento de clic al botón
toggleCartButton.addEventListener('click', function () {
    // Alternar la visibilidad del div de detalles de compra
    if (detallesCompra.style.display === 'none') {
        detallesCompra.style.display = 'block';
    } else {
        detallesCompra.style.display = 'none';
    }
});

// También, cerrar el div de detalles de compra si se hace clic fuera de él
window.addEventListener('click', function (event) {
    if (event.target !== toggleCartButton && event.target.closest('#detallesCompra') === null) {
        detallesCompra.style.display = 'none';
    }
});

//mostrar detalles

function mostrarDetalles() {
    var detallesCompra = document.getElementById('detallesCompra');
    detallesCompra.style.display = 'block';
}