$(document).ready(function(){
  let contador = 1; // Inicializar el contador en 1

  const generarIdCompra = () => {
      // Generar un ID único basado en el contador
      const id = contador;
      contador++;
      return id;
  };

  $("#agregar-pedido").click(function(){
      // Generar un nuevo ID de compra
      const idCompra = generarIdCompra();
      $("#id-compra").val(idCompra);
      $("#modal-agregar-pedido").modal('show');
  });

  $("#guardar-pedido").click(function(){
      // Obtener los valores de los campos
      const idCompra = $("#id-compra").val();
      const nombre = $("#nombre").val();
      const producto = $("#producto").val();
      const cantidad = parseInt($("#cantidad").val());
      const valor = parseFloat($("#valor").val());
      const comuna = $("#comuna").val();
      const region = $("#region").val();
      const estadoPedido = $("#estado-pedido").val();
    
      // Validar que los campos obligatorios no estén vacíos
      if (!nombre || !producto || isNaN(cantidad) || cantidad <= 0 || isNaN(valor) || valor <= 0 || !comuna || !region || !estadoPedido) {
          mostrarMensajeError("Por favor, complete todos los campos obligatorios y asegúrese de que los valores numéricos sean válidos.");
          return;
      }
    
      // Agregar el pedido a la tabla
      $("#tabla-pedidos").append(
          `<tr id="pedido-${idCompra}">
              <td>${idCompra}</td>
              <td>${nombre}</td>
              <td>${producto}</td>
              <td>${cantidad}</td>
              <td>${valor}</td>
              <td>${comuna}</td>
              <td>${region}</td>
              <td>${estadoPedido}</td>
              <td>
                  <button class="btn btn-warning btn-editar" data-id="${idCompra}">Editar</button>
                  <button class="btn btn-danger btn-eliminar" data-id="${idCompra}">Eliminar</button>
              </td>
          </tr>`
      );

      $("#modal-agregar-pedido").modal('hide');
  });

  $(document).on("click", ".btn-eliminar", function(){
      // Confirmar eliminación del pedido
      const confirmar = confirm("¿Estás seguro de que deseas eliminar este pedido?");
      if (confirmar) {
          const idCompra = $(this).data("id");
          $(`#pedido-${idCompra}`).remove();
      }
  });

  $(document).on("click", ".btn-editar", function(){
      const idCompra = $(this).data("id");
      const nombre = $(`#pedido-${idCompra} td:nth-child(2)`).text();
      const producto = $(`#pedido-${idCompra} td:nth-child(3)`).text();
      const cantidad = $(`#pedido-${idCompra} td:nth-child(4)`).text();
      const valor = $(`#pedido-${idCompra} td:nth-child(5)`).text();
      const comuna = $(`#pedido-${idCompra} td:nth-child(6)`).text();
      const region = $(`#pedido-${idCompra} td:nth-child(7)`).text();
      const estadoPedido = $(`#pedido-${idCompra} td:nth-child(8)`).text();

      // Llenar el formulario de edición con los datos del pedido seleccionado
      $("#id-compra").val(idCompra);
      $("#nombre").val(nombre);
      $("#producto").val(producto);
      $("#cantidad").val(cantidad);
      $("#valor").val(valor);
      $("#comuna").val(comuna);
      $("#region").val(region);
      $("#estado-pedido").val(estadoPedido);

      // Mostrar el botón "Modificar" y ocultar el botón "Guardar"
      $("#guardar-pedido").hide();
      $("#modificar-pedido").show();

      $("#modal-agregar-pedido").modal('show');
  });

  $("#modificar-pedido").click(function(){
      // Obtener los nuevos valores del formulario de edición
      const idCompra = $("#id-compra").val();
      const nuevoNombre = $("#nombre").val();
      const nuevoProducto = $("#producto").val();
      const nuevaCantidad = parseInt($("#cantidad").val());
      const nuevoValor = parseFloat($("#valor").val());
      const nuevaComuna = $("#comuna").val();
      const nuevaRegion = $("#region").val();
      const nuevoEstadoPedido = $("#estado-pedido").val();

      // Validar los nuevos valores
      if (!nuevoNombre || !nuevoProducto || isNaN(nuevaCantidad) || nuevaCantidad <= 0 || isNaN(nuevoValor) || nuevoValor <= 0 || !nuevaComuna || !nuevaRegion || !nuevoEstadoPedido) {
          mostrarMensajeError("Por favor, complete todos los campos obligatorios y asegúrese de que los valores numéricos sean válidos.");
          return;
      }

      // Actualizar los datos del pedido en la tabla
      $(`#pedido-${idCompra} td:nth-child(2)`).text(nuevoNombre);
      $(`#pedido-${idCompra} td:nth-child(3)`).text(nuevoProducto);
      $(`#pedido-${idCompra} td:nth-child(4)`).text(nuevaCantidad);
      $(`#pedido-${idCompra} td:nth-child(5)`).text(nuevoValor);
      $(`#pedido-${idCompra} td:nth-child(6)`).text(nuevaComuna);
      $(`#pedido-${idCompra} td:nth-child(7)`).text(nuevaRegion);
      $(`#pedido-${idCompra} td:nth-child(8)`).text(nuevoEstadoPedido);

      // Ocultar el modal de edición
      $("#modal-agregar-pedido").modal('hide');

      // Mostrar el botón "Guardar" y ocultar el botón "Modificar"
      $("#guardar-pedido").show();
      $("#modificar-pedido").hide();
  });

  const mostrarMensajeError = (mensaje) => {
      $("#mensaje-error").text(mensaje).fadeIn().delay(3000).fadeOut();
  };
});
