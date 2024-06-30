function checkRut(rut) {
    // Despejar Puntos
    var valor = rut.value.replace('.','');
    // Despejar Guión
    valor = valor.replace('-','');
    
    // Aislar Cuerpo y Dígito Verificador
    cuerpo = valor.slice(0,-1);
    dv = valor.slice(-1).toUpperCase();
    
    // Formatear RUN
    rut.value = cuerpo + '-'+ dv
    
    // Si no cumple con el mínimo ej. (n.nnn.nnn)
    if(cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false;}
    
    // Calcular Dígito Verificador
    suma = 0;
    multiplo = 2;
    
    // Para cada dígito del Cuerpo
    for(i=1;i<=cuerpo.length;i++) {
    
        // Obtener su Producto con el Múltiplo Correspondiente
        index = multiplo * valor.charAt(cuerpo.length - i);
        
        // Sumar al Contador General
        suma = suma + index;
        
        // Consolidar Múltiplo dentro del rango [2,7]
        if(multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
    }
    
    // Calcular Dígito Verificador en base al Módulo 11
    dvEsperado = 11 - (suma % 11);
    
    // Casos Especiales (0 y K)
    dv = (dv == 'K')?10:dv;
    dv = (dv == 11)?0:dv;
    
    // Validar que el Cuerpo coincide con su Dígito Verificador
    if(dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }
    
    // Si todo sale bien, eliminar errores (decretar que es válido)
    rut.setCustomValidity('');
}

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