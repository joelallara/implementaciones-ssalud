$(document).ready(function () {
    const user_input = $("#search-input")
    const search_icon = $('#search-icon')
    const search_btn = $('#search-btn')

    const ajax_div = $('#replaceable-content')
    const endpoint = '/proyectos/buscar_sql/'
    const delay_by_in_ms = 700
    let scheduled_function = false
    var pathname = window.location.pathname;

    let ajax_call = function (endpoint, request_parameters) {
        $.getJSON(endpoint, request_parameters)
            .done(response => {
                if (response['is_results']) {
                    // replace the HTML contents
                    ajax_div.html(response['html_from_view'])
                    // fade-in the div with new contents
                    ajax_div.fadeTo('slow', 1)
                    // stop animating search icon
                    search_icon.removeClass('blink')
                } else {
                    // fade out the ajax_request_div, then:
                    ajax_div.fadeTo('slow', 0).promise().then(() => {
                        // hide div with new contents
                        ajax_div.hide()
                        // stop animating search icon
                        search_icon.removeClass('blink')
                    })
                }

            })
    }


    search_btn.on('click', function () {

        const request_parameters = {
            q: user_input.val(), // value of user_input: the HTML element with ID user-input
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

    //Fill Packages list
    function packagesList(el) {
        url = $(el).data('url');
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                let rows = '';
                if (!data.packages) {
                    rows += `<p>No hay paquetes disponibles</p>`;
                } else {
                    data.packages.forEach(package => {
                        rows += `
                    <a href="#tareas-info" class="list-group-item list-group-item-action list-group-item-info"
                        data-url="{% url 'project:tasks'${package.id} %}"
                        data-id="${package.id}"
                        onClick="tasksList(this)">
                        ${package.package_name}
                    </a>`;
                    });
                }
                $("#packages-list-group").html(rows);
                $("#packages-list-group").fadeIn();
            }
        });
    };




    // Fill the projects-list-group when clic on <a> element
    $('#projects-list-group>a').click(function (e) {
        e.preventDefault();


        $("#tasks-list-group").fadeOut();

        // Remove class 'Active' to all <a> elements
        $("#projects-list-group>a.active").removeClass("active");

        $("#packages-list-group").hide();
        packagesList(this);


        // Add class 'Active' to the actual <a> element
        $(this).addClass("active");
        return false;
    });

});

//Fill Tasks list
function tasksList(el) {

    $("#tasks-list-group").hide();

    // Remove class 'Active' to all <a> elements
    $("#packages-list-group>a.active").removeClass("active");

    // Add class 'Active' to the actual <a> element
    $(el).addClass("active");

    url = $(el).data('url');
    packageId = $(el).data('id');
    $.ajax({
        url: '/proyectos/' + packageId + '/tareas',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            let rows = '';
            if (!data.tasks) {
                rows += `<p>No hay tareas disponibles</p>`;
            } else {
                data.tasks.forEach(task => {
                    rows += `
                    <a href="#" class="list-group-item list-group-item-action list-group-item-success">
                        ${task.task_name}
                    </a>`;
                });
            }
            $("#tasks-list-group").html(rows);
            $("#tasks-list-group").fadeIn();
        }
    });
};


// Fill details modal
function fillSqlModal(data) {
    $("#sqlScriptTxt").val(data.script);
    $('#sqlScriptTxt').attr('rows', data.cant_lineas);
};