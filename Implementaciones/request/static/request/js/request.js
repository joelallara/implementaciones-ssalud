class SelectPicker {
  /* 
    The djangoObject attr refers to the name of the context object in the HTML
    The djangoObjectFieldName attr refers to the name of the field of the djangoObject
  */
  constructor(id, name, djangoObject, url) {
    this.id = id;
    this.name = name;
    this.djangoObject = djangoObject;
    this.url = url;
  }

  getIdOptionSelected() {
    return $(this.id + ' option:selected').val();
  }

  getValueOptionSelected() {
    return $(this.id + ' option:selected').text();
  }

  setValueOptionSelected(value) {
    $(this.id).val(value);
  }

  // Verify if any option is selected
  isOptionSelected() {
    var optionSelected = this.getValueOptionSelected();
    if (optionSelected == '') {
      return false;
    } else {
      return true;
    }
  };

  setTitle(title) {
    $(this.id).selectpicker({
      title: title,
    });
  }

  refresh() {
    $(this.id).selectpicker('refresh');
  }

  disable() {
    $(this.id).prop('disabled', true);
  }

  enable() {
    $(this.id).prop('disabled', false);
  }

  fill() {
    var selectPicker = this;
    $.ajax({
      url: selectPicker.url,
      type: 'get',
      dataType: 'json',
      success: function (data) {
        let rows = '';
        if (data[selectPicker.name]) {
          data[selectPicker.name].forEach(object => {
            // Get the value of the modelobject_name field. Ex: project_name from Project model
            var objectFieldName = object[Object.keys(object)[4]];

            rows += `<option value="${object.id}">${objectFieldName}</option>`;
          });
          selectPicker.setTitle('-----');
        } else {
          selectPicker.setTitle('Información inexistente');
          selectPicker.disable();
        }
        $(selectPicker.id).html(rows);
        selectPicker.refresh();
      }
    });
  }
}




$(document).ready(function () {

  $("#observacionesInput").on('keyup paste', function () { // <---remove ',' comma
    var maxLength = $(this).attr('maxlength');
    var Characters = $(this).val().replace(/(<([^>]+)>)/ig, "").length; // '$' is missing from the selector
    $("#counter").text(Characters+ "/" +maxLength);

  });

  // Disable btnEnviar when submit to prevent multiples submits
  $("#implementationRequestForm").submit(function () {
    $('#btnEnviar').prop('disabled', true);
    $('.btn-cancelar').prop('disabled', true);
  });

  function disableAddButton() {
    $(".add-new").attr("disabled", "disabled");
  };

  function enableAddButton() {
    $(".add-new").removeAttr("disabled");
  };

  function disableEnviarButton() {
    $("#btnEnviar").attr("disabled", "disabled");
  };

  function enableEnviarButton() {
    $("#btnEnviar").removeAttr("disabled");
  };

  function showProjectAlert() {
    $('#projectAlert').removeClass("collapse");
  };

  function hideProjectAlert() {
    $('#projectAlert').addClass("collapse");
  };

  function showDetailAlert() {
    $('#detailAlert').removeClass("collapse");
  };

  function hideDetailAlert() {
    $('#detailAlert').addClass("collapse");
  };

  function showObservationAlert() {
    $('#observationAlert').removeClass("collapse");
  };

  function hideObservationAlert() {
    $('#observationAlert').addClass("collapse");
  };

  //Create selectpickers
  var url = $('#projectSelectpicker').data('url');
  let projectsSelectPicker = new SelectPicker('#projectSelectpicker', 'projects', 'project', url);
  let packagesSelectPicker = new SelectPicker(id = '#packageSelectpicker', name = 'packages', djangoObject = 'package');
  let tasksSelectPicker = new SelectPicker(id = '#tasksSelectpicker', name = 'tasks', 'task', djangoObject = url);

  // Fill the project SelectPicker
  projectsSelectPicker.fill();

  // Disable Package and Tasks Selecpickers
  packagesSelectPicker.disable();
  packagesSelectPicker.refresh();
  tasksSelectPicker.disable();
  tasksSelectPicker.refresh();

  // Add selectpicker bootstrap style and props
  $('select').selectpicker({
    noneResultsText: 'No se encontraron resultados'
  });

  // Gets the value of the project selectpicker
  $(projectsSelectPicker.id).change(function () {
    var isProjectSelected = projectsSelectPicker.isOptionSelected();

    // Enable or disable "Agregar" button if there is a project selected
    if (isProjectSelected) {
      var url = '/proyectos/' + projectsSelectPicker.getIdOptionSelected() + '/paquetes';
      hideProjectAlert();
      enableAddButton();


      tasksSelectPicker.setTitle('-----');
      tasksSelectPicker.refresh();

      packagesSelectPicker.url = url;
      packagesSelectPicker.fill();
      packagesSelectPicker.enable();
      packagesSelectPicker.refresh();

      enableEnviarButton();

    }
  });

  // Allows Tasks selectpicker when a package is selected
  $(packagesSelectPicker.id).change(function () {
    var isPackageSelected = packagesSelectPicker.isOptionSelected();
    if (isPackageSelected) {
      var url = '/proyectos/' + packagesSelectPicker.getIdOptionSelected() + '/tareas';
      tasksSelectPicker.url = url;
      tasksSelectPicker.fill();
      tasksSelectPicker.enable();
      tasksSelectPicker.refresh();
    }
  });

  // Verify if there is any row on #add-table
  function isTableEmpty() {
    var count = $("#table-add tbody tr").length;
    if (count >= 1) {
      return false;
    } else {
      return true;
    }
  };



  // Enable o Disable "Enviar" button if is or not a project selected or if there is no row on add-table
  $("#btnEnviar").click(function () {
    var isProjectSelected = projectsSelectPicker.isOptionSelected();
    if (!isProjectSelected) {
      showProjectAlert();
      disableAddButton();
      disableEnviarButton();
      return false;
    } else {
      hideProjectAlert();
      enableAddButton();
      projectsSelectPicker.refresh();
      if (isTableEmpty()) {
        showDetailAlert();
        disableEnviarButton();
        return false;
      } else {
        hideDetailAlert();
        enableEnviarButton();
      }
    }
  });

  var rowIndex = 0;
  // Append table detail row
  $(".add-new").click(function () {
    var isProjectSelected = projectsSelectPicker.isOptionSelected();

    if (isProjectSelected) {
      enableAddButton();
    } else {
      showProjectAlert();
      disableAddButton();
      disableEnviarButton();
      return;
    }

    var observation = $.trim($("#observacionesInput").val());
    var index = $("#table-add tbody tr:last-child").index();
    var selectedProject = $(projectsSelectPicker.id + ' option:selected').val();
    var values = [];

    // Add the project name to the detail tittle
    $('#tituloDetalle').text = 'Detalle Solicitud';

    // Create Package Detail Row
    var selectedPackage;
    var packageDetailRow;
    if (packagesSelectPicker.isOptionSelected()) {
      selectedPackage = packagesSelectPicker.getValueOptionSelected() ;
      packageDetailRow = selectedPackage +
        '<input type="hidden" value="' + selectedPackage + rowIndex + '" name="package"/>';
    } else {
      selectedPackage = '-----' + rowIndex;
      packageDetailRow = '-----' +
        '<input type="hidden" value="' + selectedPackage + '" name="package"/>';
    }

    // Create Tasks Detail Row
    var tasks;
    var tasksDetailRow;
    if (tasksSelectPicker.isOptionSelected()) {
      tasks = '<ol>';
      var selectedTasks = $(tasksSelectPicker.id).find('option:selected');
      selectedTasks.each(function () {
        values.push('<li>' + $(this).text() +
          '</li><input type="hidden" value="' +
          $(this).text() + '" name="' + selectedPackage + rowIndex + 'task"/>');
      });
      tasks += values.join("");
      tasks += '</ol>';
      tasksDetailRow = '<td class="text-left align-middle">' + tasks + '</td>';
    } else {
      tasks = '-----';
      tasksDetailRow = '<td class="text-center align-middle">' +
        tasks +
        '<input type="hidden" value="' + tasks + '" name="' + selectedPackage + rowIndex + 'task"/>' +
        '</td>';
    }

    // Create Observation Detail Row
    var observationDetailRow;
    if (observation) {
      hideObservationAlert();
      observationDetailRow =
        '<td class="text-left align-middle ObservationDetailRow">' +
        observation +
        '<input type="hidden" id="ObHiddenInput" value="' + observation + '" name="' + selectedPackage + rowIndex + 'observations"/>' +
        '</td>';
    } else {
      showObservationAlert();
      return;
    }

    //Create Detail table row
    var row = '<tr id="detailRow">' +
      '<td class="text-center align-middle">' +
      packageDetailRow +
      '</td>' +
      tasksDetailRow +
      observationDetailRow +
      '<td class="text-center align-middle">' +
      '<a class="add" title="Actualizar observacion" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a>' +
      '<a class="edit" title="Editar observacion" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a>' +
      '<a class="delete" title="Borrar" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>' +
      '</td>' +
      '</tr>';
    $("#table-add").append(row);
    $("#table-add tbody tr").eq(index + 4).find(".delete").toggle();


    if (isTableEmpty()) {
      disableEnviarButton();
      projectsSelectPicker.enable();
      projectsSelectPicker.refresh();
    } else {
      enableEnviarButton();
      $('#table-add').show();
      projectsSelectPicker.disable();
      projectsSelectPicker.refresh();
      hideDetailAlert();
    }


    // Reset form
    $('#implementationRequestForm').trigger("reset");

    // Keeps the value of the selected project
    projectsSelectPicker.setValueOptionSelected(selectedProject);

    // Set the id value on the hidden input to pass it through POST request
    $('#selectedProjectid').val(selectedProject);

    // Refresh selectpickers
    projectsSelectPicker.refresh();
    packagesSelectPicker.refresh();
    tasksSelectPicker.refresh();

    $("#counter").text("0/500");

    rowIndex++;
  });

  // Delete row from add-table
  var deleteRow = function (row) {
    row.remove();
  };

  // Delete row on delete button click
  $(document).on("click", ".delete", function () {
    var row = $(this).parents("tr");
    deleteRow(row);

    if (isTableEmpty() == true) {
      projectsSelectPicker.enable();
      projectsSelectPicker.refresh();
    }
  });

  // Add row on add button click
  $(document).on("click", ".add", function () {
    var buttonAdd = $(this);
    var empty = false;
    var input = $(this).parents("tr").find('input[type="text"]');
    var hiddenInput = $(this).parents("tr").find('#ObHiddenInput');
    var count = 0;
    input.each(function () {
      if (!$(this).val()) {
        $(this).addClass("error");
        empty = true;
      } else {
        $(this).removeClass("error");
        $(this).parents("tbody").find(".add").each(function () {
          // Increment count when a obs is in edit mode
          if ($(this).css('display') != 'none') {
            count++;
          }
        });
      }
    });
    $(this).parents("tr").find(".error").first().focus();
    if (!empty) {
      input.each(function () {
        $(this).parent("td").html($(this).val());
        hiddenInput.val($(this).val());
        buttonAdd.parents("tr").find(".ObservationDetailRow").append(hiddenInput);
      });
      $(this).parents("tr").find(".add, .edit").toggle();
      // Show delete button when there is no row editing
      $(this).parents("tbody").find(".delete").each(function () {
        $(this).css("display", "inline-block")
      });
      // If count 1 then there are not obs being editing it allows to send the form. Never will be 0 because its count before toggle the button add
      if (count == 1) {
        $(".add-new").removeAttr("disabled");
        $('#btnEnviar').prop('disabled', false);
        // Disable all edit buttons except the clicked
        $(this).parents("tbody").find(".edit").not($(this)).css("display", "inline-block");
      }
    }
  });

  // Edit row on edit button click
  $(document).on("click", ".edit", function () {

    // Disable all edit buttons except the clicked
    $(this).parents("tbody").find(".edit, .delete").not($(this)).css("display", "none");

    $(this).parents("tr").find(".ObservationDetailRow").each(function () {
      var hiddenInput = $(this).find('#ObHiddenInput');
      $(this).html('<input type="text" class="form-control" maxlength = "500" value="' + $(this).text() + '">');
      $(this).append(hiddenInput);
    });
    $(this).parents("tr").find(".add, .edit").toggle();
    // Disable add-new and btnEnviar when editing a row
    $(".add-new").attr("disabled", "disabled");
    $('#btnEnviar').prop('disabled', true);
  });

});

//Fill Details Modal
function fillDetailsModal(el) {
  packageId = $(el).data('id');
  url = $(el).data('url');
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    success: function (data) {
      let rows = '';
      if (!data.details) {
        rows += `
        <tr>
          <td colspan="3">No hay detalles disponibles</td>
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


const user_input = $("#search-input")
const search_icon = $('#search-icon')
const initial_request_div = $('#initial-content')
const ajax_request_div = $('#replaceable-content')
const pagination = $('#pagination-row')
const endpoint = '/solicitudes/buscar/'
const delay_by_in_ms = 700
let scheduled_function = false
var pathname = window.location.pathname;

let ajax_call = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters)
    .done(response => {
      if (response['is_requests']) {
        // fade out the initial_request_div, then:
        initial_request_div.fadeTo('slow', 0).promise().then(() => {
          // hide original request table
          initial_request_div.hide()
          // hide pagination
          pagination.hide()
          // replace the HTML contents
          ajax_request_div.html(response['html_from_view'])
          // fade-in the div with new contents
          ajax_request_div.fadeTo('slow', 1)
          // stop animating search icon
          search_icon.removeClass('blink')
        })
      } else {
        // fade out the ajax_request_div, then:
        ajax_request_div.fadeTo('slow', 0).promise().then(() => {
          // hide div with new contents
          ajax_request_div.hide()
          // fade-in the initial_request_div
          initial_request_div.fadeTo('slow', 1)
          // show pagination and div initial_request_div
          pagination.fadeTo('slow', 1).promise().then(() => {
            // hide original request table
            initial_request_div.show()
            pagination.show()
          })
          // stop animating search icon
          search_icon.removeClass('blink')
        })
      }

    })
}


user_input.on('keyup', function () {

  const request_parameters = {
    q: $(this).val(), // value of user_input: the HTML element with ID user-input
    path: pathname // value of path to determine wich is the correct view to show
  }

  // start animating the search icon with the CSS class
  search_icon.addClass('blink')

  // if scheduled_function is NOT false, cancel the execution of the function
  if (scheduled_function) {
    clearTimeout(scheduled_function)
  }

  // setTimeout returns the ID of the function to be executed
  scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})