$(".x-drop-down__value").click(function(event) {
  toggleMenu();
  event.stopPropagation();
});

$('.b-drop-down__list-item').click(function() {
  $('.x-drop-down__value').html($(this).text());
  toggleMenu();
});

function toggleMenu() {
  let menu = $(".x-drop-down__dropped");
  if (!menu.hasClass('active')) {
    window.addEventListener('click', closeMenu);
  } else {
    window.removeEventListener('click', closeMenu);
  }
  menu.toggleClass("active");
}

function closeMenu() {
  $(".x-drop-down__dropped").removeClass("active")
}

$('.x-drop-down__dropped').click(function(event) {
  event.stopPropagation();
});


$('.x-input__field').on('input', function() { 
  let search = $(this).val();
  searchData(search);
});

function searchData(search) {
  let towns = $('.b-drop-down__list-item');
  towns.each(function() {
    if ($(this).text().indexOf(search) === -1) {
      $(this).addClass('item_hide');
    } else {
      $(this).removeClass('item_hide');
    }
  });
}