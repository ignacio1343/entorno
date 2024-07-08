$(document).ready(function(){
    let contador = 1; // Inicializar el contador en 1

    const generarIdProducto = () => {
        // Generar un ID único basado en el contador
        const id = contador;
        contador++;
        return id;
    };

    $("#agregar-producto").click(function(){
        // Generar un nuevo ID de producto
        const idProducto = generarIdProducto();
        $("#id-producto").val(idProducto);
        $("#imagen").val(''); // Limpiar el campo de carga de imagen
        $("#modal-agregar-producto").modal('show');
    });

    $("#guardar-producto").click(function(){
        // Obtener los valores de los campos
        const idProducto = $("#id-producto").val();
        const nombre = $("#nombre").val();
        const tipo = $("#tipo").val();
        const stock = parseInt($("#stock").val());
        const valor = parseFloat($("#valor").val());
        const imagen = $("#imagen").prop('files')[0]; // Obtener el archivo de imagen

        // Validar que los campos obligatorios no estén vacíos
        if (!nombre || !tipo || isNaN(stock) || stock <= 0 || isNaN(valor) || valor <= 0 || !imagen) {
            mostrarMensajeError("Por favor, complete todos los campos obligatorios y asegúrese de que los valores numéricos sean válidos.");
            return;
        }

        // Crear un objeto de tipo FileReader para leer el contenido de la imagen
        const reader = new FileReader();

        // Definir la acción que se realizará cuando la imagen se cargue completamente
        reader.onload = function(event) {
            // Agregar el producto a la tabla con la URL de la imagen
            $("#tabla-productos").append(
                `<tr id="producto-${idProducto}">
                    <td>${idProducto}</td>
                    <td>${nombre}</td>
                    <td>${tipo}</td>
                    <td>${stock}</td>
                    <td>${valor}</td>
                    <td><img src="${event.target.result}" alt="imagen" style="max-width: 100px; max-height: 100px;"></td>
                    <td>
                        <button class="btn btn-warning btn-editar" data-id="${idProducto}">Editar</button>
                        <button class="btn btn-danger btn-eliminar" data-id="${idProducto}">Eliminar</button>
                    </td>
                </tr>`
            );
        };

        // Leer el contenido de la imagen como una URL
        reader.readAsDataURL(imagen);

        $("#modal-agregar-producto").modal('hide');
    });

    $(document).on("click", ".btn-eliminar", function(){
        // Confirmar eliminación del producto
        const confirmar = confirm("¿Estás seguro de que deseas eliminar este producto?");
        if (confirmar) {
            const idProducto = $(this).data("id");
            $(`#producto-${idProducto}`).remove();
        }
    });

    $(document).on("click", ".btn-editar", function(){
        const idProducto = $(this).data("id");
        const nombre = $(`#producto-${idProducto} td:nth-child(2)`).text();
        const tipo = $(`#producto-${idProducto} td:nth-child(3)`).text();
        const stock = $(`#producto-${idProducto} td:nth-child(4)`).text();
        const valor = $(`#producto-${idProducto} td:nth-child(5)`).text();

        // Llenar el formulario de edición con los datos del producto seleccionado
        $("#id-producto").val(idProducto);
        $("#nombre").val(nombre);
        $("#tipo").val(tipo);
        $("#stock").val(stock);
        $("#valor").val(valor);

        // Mostrar el botón "Modificar" y ocultar el botón "Guardar"
        $("#guardar-producto").hide();
        $("#modificar-producto").show();

        $("#modal-agregar-producto").modal('show');
    });

    $("#modificar-producto").click(function(){
        // Obtener los nuevos valores del formulario de edición
        const idProducto = $("#id-producto").val();
        const nuevoNombre = $("#nombre").val();
        const nuevoTipo = $("#tipo").val();
        const nuevoStock = parseInt($("#stock").val());
        const nuevoValor = parseFloat($("#valor").val());
        const imagen = $("#imagen").prop('files')[0]; // Obtener el archivo de imagen

        // Validar los nuevos valores
        if (!nuevoNombre || !nuevoTipo || isNaN(nuevoStock) || nuevoStock <= 0 || isNaN(nuevoValor) || nuevoValor <= 0) {
            mostrarMensajeError("Por favor, complete todos los campos obligatorios y asegúrese de que los valores numéricos sean válidos.");
            return;
        }

        // Crear un objeto de tipo FileReader para leer el contenido de la imagen
        const reader = new FileReader();

        // Definir la acción que se realizará cuando la imagen se cargue completamente
        reader.onload = function(event) {
            // Actualizar los datos del producto en la tabla, incluyendo la nueva imagen
            $(`#producto-${idProducto} td:nth-child(2)`).text(nuevoNombre);
            $(`#producto-${idProducto} td:nth-child(3)`).text(nuevoTipo);
            $(`#producto-${idProducto} td:nth-child(4)`).text(nuevoStock);
            $(`#producto-${idProducto} td:nth-child(5)`).text(nuevoValor);
            $(`#producto-${idProducto} td:nth-child(6) img`).attr('src', event.target.result); // Actualizar la imagen

            // Ocultar el modal de edición
            $("#modal-agregar-producto").modal('hide');

            // Mostrar el botón "Guardar" y ocultar el botón "Modificar"
            $("#guardar-producto").show();
            $("#modificar-producto").hide();
        };

        // Leer el contenido de la imagen como una URL
        reader.readAsDataURL(imagen);
    });

    const mostrarMensajeError = (mensaje) => {
        $("#mensaje-error").text(mensaje).fadeIn().delay(3000).fadeOut();
    };
});
