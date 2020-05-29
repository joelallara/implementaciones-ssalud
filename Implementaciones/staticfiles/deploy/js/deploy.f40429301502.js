//Fill Deploy Modal
function fillDeployModal(el) {
  header = $(el).data('id');
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
          <td colspan="3">No hay detalles disponibles</td>
        </tr>`;
      } else {
        $("#requestHeader").val(data.header);
        $("#requestProject").text(data.project_name);
        $("#requestDate").text(data.created);
        $("#requestUser").text(data.created_by);
      }
    }
  });
};

$(document).ready(function () {
  $("#deployForm").submit(function (e) {
    e.preventDefault();
  });
});