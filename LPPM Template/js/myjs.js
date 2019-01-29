// WOW JS
  new WOW().init();

// materialize DOM
  const sideNav = document.querySelectorAll('.sidenav');
  M.Sidenav.init(sideNav);

  const parallax = document.querySelectorAll('.parallax');
  M.Parallax.init(parallax);

  const scroll = document.querySelectorAll('.scrollspy');
  M.ScrollSpy.init(scroll, {
    scrollOffset: 50
  });

  const dropdown = document.querySelectorAll('.dropdown-button');
  M.Dropdown.init(dropdown,{
    coverTrigger: false
  });

  const collapSible = document.querySelectorAll('.collapsible');
  M.Collapsible.init(collapSible);

  const modalbtn = document.querySelectorAll('.modal');
  M.Modal.init(modalbtn);

  const tahun= document.querySelectorAll('.datepicker');
  M.Datepicker.init(tahun);



  // navbar
  $(window).on('scroll',function(){
    if ($(window).scrollTop()) {
          $('nav').addClass('blue darken-4');       
    } else {
          $('nav').removeClass('blue darken-4'); 
    }
  });

  // textarea
  $('#textarea1').val('');
  M.textareaAutoResize($('#textarea1'));




