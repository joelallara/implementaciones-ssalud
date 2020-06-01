$(window).resize(function () {
  var width = $(window).width();
  if (width < 500) {
    $('.table').addClass('table-responsive');
  } else if (width > 500){
    $('.table').removeClass('table-responsive');
  }
});
