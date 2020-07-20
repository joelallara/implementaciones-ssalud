//Fill Deploy Modal
function fillDeployModal(el) {
  header = $(el).data('id');
  url = $(el).data('url');
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function (data) {
      if (data) {
        $("#requestHeader").val(data.header);
        $("#requestProject").text(data.project_name);
        $("#requestDate").text(data.created);
        $("#requestUser").text(data.created_by);
      }
    }
  });
};


$(document).ready(function () {
  // Disable btnEnviarDeploy when submit to prevent multiples submits
  $("#deployForm").submit(function () {
    $('#btnEnviarDeploy').prop('disabled', true);
    $('.btn-cancelar').prop('disabled', true);
  });

  //Focus in LSN input when deploy modal is shown
  $('#modalDeploy').on('shown.bs.modal', function() {
    $('#lsn').focus();
  })
});




const user_input_deploy = $("#search-input-deploy")
const search_icon_deploy = $('#search-icon')
const initial_request_div_deploy = $('#initial-content')
const ajax_request_div_deploy = $('#replaceable-content')
const pagination_deploy = $('#pagination-row')
const endpoint_deploy = '/implementaciones/buscar/'
const delay_by_in_ms_deploy = 700
let scheduled_function_deploy = false

let ajax_call_deploy = function (endpoint_deploy, request_parameters_deploy) {
  $.getJSON(endpoint_deploy, request_parameters_deploy)
    .done(response => {
      if (response['is_deploys']) {
        // fade out the initial_request_div, then:
        initial_request_div_deploy.fadeTo('slow', 0).promise().then(() => {
          // hide original request table
          initial_request_div_deploy.hide()
          // hide pagination
          pagination_deploy.hide()
          // replace the HTML contents
          ajax_request_div_deploy.html(response['html_from_view'])
          // fade-in the div with new contents
          ajax_request_div_deploy.fadeTo('slow', 1)
          // stop animating search icon
          search_icon_deploy.removeClass('blink')
        })
      } else {
        // fade out the ajax_request_div, then:
        ajax_request_div_deploy.fadeTo('slow', 0).promise().then(() => {
          // hide div with new contents
          ajax_request_div_deploy.hide()
          // fade-in the initial_request_div
          initial_request_div_deploy.fadeTo('slow', 1)
          // show pagination and div initial_request_div
          pagination_deploy.fadeTo('slow', 1).promise().then(() => {
            // hide original request table
            initial_request_div_deploy.show()
            pagination_deploy.show()
          })
          // stop animating search icon
          search_icon_deploy.removeClass('blink')
        })
      }

    })
}


user_input_deploy.on('keyup', function () {

  const request_parameters_deploy = {
    q: $(this).val(), // value of user_input: the HTML element with ID user-input
  }

  // start animating the search icon with the CSS class
  search_icon_deploy.addClass('blink')

  // if scheduled_function is NOT false, cancel the execution of the function
  if (scheduled_function_deploy) {
    clearTimeout(scheduled_function_deploy)
  }

  // setTimeout returns the ID of the function to be executed
  scheduled_function_deploy = setTimeout(ajax_call_deploy, delay_by_in_ms_deploy, endpoint_deploy, request_parameters_deploy)
})