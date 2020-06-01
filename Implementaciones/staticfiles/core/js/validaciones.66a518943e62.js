(
  function ctrlSubmit(formulario){
    formulario.disabled=true;
    formulario.form.submit();
  }

);

$(window).resize(function() {
  var width = $(window).width();
  if (width < 480){
    alert('Your screen is too small');
  }
});
