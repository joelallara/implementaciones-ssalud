
$(document).ready(function () {

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
                    <a href="#" class="list-group-item list-group-item-action"
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
                    <a href="#" class="list-group-item list-group-item-action">
                        ${task.task_name}
                    </a>`;
                });
            }
            $("#tasks-list-group").html(rows);
            $("#tasks-list-group").fadeIn();
            //$("#tasks-list-group").show();
        }
    });
};
