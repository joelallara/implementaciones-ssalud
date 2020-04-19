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

  //Create selectpickers
  var url = $('#projectSelectpicker').data('url');
  let projectsSelectPicker = new SelectPicker('#projectSelectpicker', 'projects', 'project', url);
  let packagesSelectPicker = new SelectPicker(id='#packageSelectpicker', name='packages', djangoObject='package',);
  let tasksSelectPicker = new SelectPicker(id='#tasksSelectpicker', name='tasks', 'task', djangoObject=url);

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
      $("span.project").removeClass("error");
      $(".add-new").removeAttr("disabled");


      tasksSelectPicker.setTitle('-----');
      tasksSelectPicker.refresh();

      packagesSelectPicker.url = url;
      packagesSelectPicker.fill();
      packagesSelectPicker.enable();
      packagesSelectPicker.refresh();

      
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
  var isTableEmpty = function () {
    var count = $("#table-add tbody tr").length;
    if (count >= 1) {
      return false;
    } else {
      return true;
    }
  };

  // Append table with add row form on add new button click
  $(".add-new").click(function () {
    var isProjectSelected = projectsSelectPicker.isOptionSelected();
    $('.container-fluid').find(".error").focus();

    if (isProjectSelected) {
      $(".add-new").removeAttr("disabled");
      projectsSelectPicker.disable();
      projectsSelectPicker.refresh();
    } else {
      $("span.project").addClass("error");
      $(".add-new").attr("disabled", "disabled");
      //return;
      return;
    }

    var observation = $.trim($("#observacionesInput").val());
    var index = $("#table-add tbody tr:last-child").index();
    // var selectedProject = packagesSelectPicker.getValueOptionSelected();
    var selectedProject = $(projectsSelectPicker.id + ' option:selected').val();
    var selectedPackage = packagesSelectPicker.getValueOptionSelected();
    var selectedTasks = $(tasksSelectPicker.id).find('option:selected');
    var values = [];

    selectedTasks.each(function () {
      values.push('<li>' + $(this).text());
    });
    tasks = values.join("</li>");
    var row = '<tr>' +
      '<td class="text-center align-middle">' +
      selectedPackage +
      '</td>' +
      '<td class="text-left align-middle">' +
      '<ol>' +
      tasks +
      '<ol>' +
      '</td>' +
      '<td class="text-justify align-middle">' +
      observation +
      '</td>' +
      '<td class="text-center align-middle">' +
      '<a class="delete" title="Delete"><i class="material-icons">&#xE872;</i></a>' +
      '</td>' +
      '</tr>';
    $("#table-add").append(row);
    $("#table-add tbody tr").eq(index + 4).find(".delete").toggle();

    if (!isTableEmpty()) {
      $('#table-add').show();
    }

    
    // Reset form
    $('#implementationRequestForm').trigger("reset");

    // Keeps the value of the selected project
    projectsSelectPicker.setValueOptionSelected(selectedProject);

    // Refresh selectpickers
    projectsSelectPicker.refresh();
    packagesSelectPicker.refresh();
    tasksSelectPicker.refresh();


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

});

//Fill Details Modal
function fillDetailsModal(el) {
  $('#modal1').modal('hide');
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
