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

  // Verify if any option is selected
  isOptionSelected() {
    if (this.getValueOptionSelected == "") {
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
    if (!isProjectSelected) {
      $("span.project").addClass("error");
      $(".add-new").attr("disabled", "disabled");
      //return;
    } else {
      var url = '/proyectos/' + projectsSelectPicker.getIdOptionSelected() + '/paquetes';
      $("span.project").removeClass("error");
      $(".add-new").removeAttr("disabled");
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
      // If not project selected exit
      return;
    }

    var observation = $.trim($("#observaciones").val());
    var index = $("#table-add tbody tr:last-child").index();
    var selectedPackage = packagesSelectPicker.getValueOptionSelected(); $("#packageSelectpicker option:selected").text();
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

    $('#implementationRequestForm').trigger("reset");
    packagesSelectPicker.refresh();
    tasksSelectPicker.refresh();
    $('select[name=projectSelectpicker]').val(selectedProject);
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

//Fill the provided Selectpicker
// function fillSelectPicker(selectPicker) {
//   if (selectPicker == 'projects') {
//     var url = $('#projectSelectpicker').data('url');
//     var selectPickerId = "#projectSelectpicker";
//   } else if (selectPicker == 'packages') {
//     var projectIdSelected = $('#projectSelectpicker option:selected').val();
//     var url = '/proyectos/' + projectIdSelected + '/paquetes';
//     var selectPickerId = "#packageSelectpicker";
//   } else if (selectPicker == 'tasks') {
//     var packageId = $('#packageSelectpicker option:selected').val();
//     var url = '/proyectos/' + packageId + '/tareas';
//     var selectPickerId = "#tasksSelectpicker";
//   }

//   $.ajax({
//     url: url,
//     type: 'get',
//     dataType: 'json',
//     success: function (data) {
//       let rows = '';
//       if (data[selectPicker]) {
//         if (selectPicker == 'projects') {
//           data.projects.forEach(project => {
//             rows += `<option value="${project.id}">${project.project_name}</option>`;
//           });
//         } else if (selectPicker == 'packages') {
//           data.packages.forEach(package => {
//             rows += `<option value="${package.id}">${package.package_name}</option>`;
//           });
//         } else if (selectPicker == 'tasks') {
//           data.tasks.forEach(task => {
//             rows += `<option value="${task.id}">${task.task_name}</option>`;
//           });
//         }
//         $(selectPickerId).selectpicker({
//           title: '-----',
//         });
//       } else {
//         $(selectPickerId).selectpicker({
//           title: 'Información inexistente',
//         });
//       }

//       $(selectPickerId).html(rows);
//       $(selectPickerId).selectpicker('refresh');
//     }
//   });
// }

//Fills the project selectPicker
// fillSelectPicker('projects');


// // Disable Package and Tasks Selecpicker
// $("#packageSelectpicker").prop('disabled', true);
// $('#packageSelectpicker').selectpicker('refresh');
// $("#tasksSelectpicker").prop('disabled', true);
// $('#tasksSelectpicker').selectpicker('refresh');

// // Add selectpicker bootstrap style and props
// $('select').selectpicker({
//   noneResultsText: 'No se encontraron resultados'
// });

// Gets the value of the project selectpicker
// var selectedProject = $("#projectSelectpicker option:selected").text();
// $("#projectSelectpicker").change(function () {
//   fillSelectPicker('packages');
//   selectedProject = $("#projectSelectpicker option:selected").text();
//   projectSelect(selectedProject);
//   $("#packageSelectpicker").prop('disabled', false);
//   $('#packageSelectpicker').selectpicker('refresh');
// });

// Allows Tasks selectpicker when a package is selected
// $("#packageSelectpicker").change(function () {
//   fillSelectPicker('tasks');
//   $("#tasksSelectpicker").prop('disabled', false);
//   $('#tasksSelectpicker').selectpicker('refresh');
// });



// // Gets the value of the tasks selectpicker
// // selectedTasks = $("#tasksSelectpicker option:selected").text();
// // $("#tasksSelectpicker").change(function () {
// //   selectedTasks = $("#tasksSelectpicker option:selected").text();
// //   console.log(selectedTasks)
// // });




// Verify if there is any row on #add-table
// var isTableEmpty = function () {
//   var count = $("#table-add tbody tr").length;
//   if (count >= 1) {
//     return false;
//   } else {
//     return true;
//   }
// };

// // Verify if any project is selected
// var isProjectSelected = function (selectedProject) {
//   if (selectedProject == "") {
//     return false;
//   } else {
//     return true;
//   }
// };

// // Enable or disable "Agregar" button if there is a project selected
// var projectSelect = function (selectedProject) {
//   if (!isProjectSelected(selectedProject)) {
//     $("span.project").addClass("error");
//     $(".add-new").attr("disabled", "disabled");
//     return;
//   } else {
//     $("span.project").removeClass("error");
//     $(".add-new").removeAttr("disabled");
//   }
// };

// // Append table with add row form on add new button click
// $(".add-new").click(function () {
//   var project = projectSelect(selectedProject)
//   $('.container-fluid').find(".error").focus();

//   //Check if there is a project selected on selectpicker
//   if (isProjectSelected(project)) {
//     $(".add-new").removeAttr("disabled");
//     $("#projectSelectpicker").prop('disabled', true);
//     $('#projectSelectpicker').selectpicker('refresh');
//   } else {
//     return;
//   }

//   var observation = $.trim($("#observaciones").val());
//   var index = $("#table-add tbody tr:last-child").index();
//   var selectedPackage = $("#packageSelectpicker option:selected").text();
//   var selectedTasks = $("#tasksSelectpicker").find('option:selected');
//   var values = [];
//   selectedTasks.each(function () {
//     values.push('<li>' + $(this).text());
//   });
//   tasks = values.join("</li>");
//   var row = '<tr>' +
//     '<td class="text-center align-middle">' +
//     selectedPackage +
//     '</td>' +
//     '<td class="text-left align-middle">' +
//     '<ol>' +
//     tasks +
//     '<ol>' +
//     '</td>' +
//     '<td class="text-justify align-middle">' +
//     observation +
//     '</td>' +
//     '<td class="text-center align-middle">' +
//     '<a class="delete" title="Delete"><i class="material-icons">&#xE872;</i></a>' +
//     '</td>' +
//     '</tr>';
//   $("#table-add").append(row);
//   $("#table-add tbody tr").eq(index + 4).find(".delete").toggle();

//   if (!isTableEmpty()) {
//     $('#table-add').show();
//   }

//   $('#implementationRequestForm').trigger("reset");
//   $("#packageSelectpicker").selectpicker("refresh");
//   $("#tasksSelectpicker").selectpicker("refresh");
//   $('select[name=projectSelectpicker]').val(selectedProject);
// });

// // Delete row from add-table
// var deleteRow = function (row) {
//   row.remove();
// };

// // Delete row on delete button click
// $(document).on("click", ".delete", function () {
//   var row = $(this).parents("tr");
//   deleteRow(row);

//   if (isTableEmpty() == true) {
//     $("#projectSelectpicker").prop('disabled', false);
//     $('#projectSelectpicker').selectpicker('refresh');
//   }
// });

// });

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
