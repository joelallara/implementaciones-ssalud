//Fill Tasks Modal
function getDetails(el) {
  $('#modal1').modal('hide');
  packageId = $(el).data('id');
  url = $(el).data('url');
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function (data) {
      let rows = '';
      if (!data) {
        rows += `
          <tr>
            <td colspan="5">No hay detalles disponibles</td>
          </tr>`;
      } else {
        data.details.forEach(detail => {
          rows += `
          <tr>
            <td class="text-center align-middle">${detail.package}</td>
            <td class="text-center align-middle">${detail.tasks}</td>
            <td class="text-center align-middle">${detail.observations}</td>
          </tr>`;
        });
      }
      $("#table-details > tbody").html(rows);
    }
  });
};