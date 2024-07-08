$(document).ready(function(){

    $("#agregar-usuario").click(function(){
        $("#rut").val("");
        $("#nombre").val("");
        $("#apellido").val("");
        $("#usuario").val("");
        $("#correo").val("");
        $("#contrasena").val("");
        $("#comuna").val("");
        $("#region").val("");
        $("#modal-agregar-usuario").modal('show');
    });


    $("#guardar-usuario").click(function(){
        // Obtener los valores de los campos
        const rut = $("#rut").val();
        const nombre = $("#nombre").val();
        const apellido = $("#apellido").val();
        const usuario = $("#usuario").val();
        const correo = $("#correo").val();
        const contrasena = $("#contrasena").val();
        const comuna = $("#comuna").val();
        const region = $("#region").val();
    
        // Validar que los campos obligatorios no estén vacíos
        // Expresión regular para validar el formato del RUT
        var rutRegex = /^\d{7,8}-[0-9Kk]$/;

// Expresión regular para validar solo letras
        var letrasRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;

        // Validación del RUT, nombre, apellido y correo electrónico
        if (!rut || !nombre || !apellido || !usuario || !correo || !contrasena || !comuna || !region || !rutRegex.test(rut) || !letrasRegex.test(nombre) || !letrasRegex.test(apellido)) {
            mostrarMensajeError("Por favor, complete todos los campos obligatorios. Asegúrese de que el RUT tenga el formato correcto (ejemplo: 12345678-9), que el nombre y apellido contengan solo letras, y que el correo electrónico tenga un formato válido.");
            return;
        }
    
        // Agregar el usuario a la tabla
        $("#tabla-usuarios").append(
            `<tr>
                <td>${rut}</td>
                <td>${nombre}</td>
                <td>${apellido}</td>
                <td>${usuario}</td>
                <td>${correo}</td>
                <td>${contrasena}</td>
                <td>${comuna}</td>
                <td>${region}</td>
                <td>
                    <button class="btn btn-warning btn-editar-usuario" data-id="${rut}">Editar</button>
                    <button class="btn btn-danger btn-eliminar-usuario" data-id="${rut}">Eliminar</button>
                </td>
            </tr>`
        );

        $("#modal-agregar-usuario").modal('hide');
    });

    $(document).on("click", ".btn-eliminar-usuario", function(){
        // Confirmar eliminación del usuario
        const confirmar = confirm("¿Estás seguro de que deseas eliminar este usuario?");
        if (confirmar) {
            $(this).closest("tr").remove();
        }
    });

    $(document).on("click", ".btn-editar-usuario", function(){
        const $fila = $(this).closest("tr");
        const rut = $fila.find("td:nth-child(1)").text();
        const nombre = $fila.find("td:nth-child(2)").text();
        const apellido = $fila.find("td:nth-child(3)").text();
        const usuario = $fila.find("td:nth-child(4)").text();
        const correo = $fila.find("td:nth-child(5)").text();
        const contrasena = $fila.find("td:nth-child(6)").text();
        const comuna = $fila.find("td:nth-child(7)").text();
        const region = $fila.find("td:nth-child(8)").text();

        // Llenar el formulario de edición con los datos del usuario seleccionado
        $("#rut").val(rut);
        $("#nombre").val(nombre);
        $("#apellido").val(apellido);
        $("#usuario").val(usuario);
        $("#correo").val(correo);
        $("#contrasena").val(contrasena);
        $("#comuna").val(comuna);
        $("#region").val(region);

        // Mostrar el botón "Modificar" y ocultar el botón "Guardar"
        $("#guardar-usuario").hide();
        $("#modificar-usuario").show();

        $("#modal-agregar-usuario").modal('show');
    });

    $("#modificar-usuario").click(function(){
        const rut = $("#rut").val();

        // Obtener los nuevos valores del formulario de edición
        const nuevoNombre = $("#nombre").val();
        const nuevoApellido = $("#apellido").val();
        const nuevoUsuario = $("#usuario").val();
        const nuevoCorreo = $("#correo").val();
        const nuevaContrasena = $("#contrasena").val();
        const nuevaComuna = $("#comuna").val();
        const nuevaRegion = $("#region").val();

        // Validar los nuevos valores
        if (!nuevoNombre || !nuevoApellido || !nuevoUsuario || !nuevoCorreo || !nuevaContrasena || !nuevaComuna || !nuevaRegion) {
            mostrarMensajeError("Por favor, complete todos los campos obligatorios.");
            return;
        }

        // Actualizar los datos del usuario en la tabla
        const $fila = $(`#tabla-usuarios tr:has(td:contains('${rut}'))`);
        $fila.find("td:nth-child(2)").text(nuevoNombre);
        $fila.find("td:nth-child(3)").text(nuevoApellido);
        $fila.find("td:nth-child(4)").text(nuevoUsuario);
        $fila.find("td:nth-child(5)").text(nuevoCorreo);
        $fila.find("td:nth-child(6)").text(nuevaContrasena);
        $fila.find("td:nth-child(7)").text(nuevaComuna);
        $fila.find("td:nth-child(8)").text(nuevaRegion);

        // Ocultar el modal de edición
        $("#modal-agregar-usuario").modal('hide');

        // Mostrar el botón "Guardar" y ocultar el botón "Modificar"
        $("#guardar-usuario").show();
        $("#modificar-usuario").hide();
    });

    const mostrarMensajeError = (mensaje) => {
        $("#mensaje-error").text(mensaje).fadeIn().delay(3000).fadeOut();
    };
});

