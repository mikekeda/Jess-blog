$(document).ready(function() {
  function set_active_link (link) {
    var a_selector = 'a[href="' + link + '"]';
    var $link = $(a_selector);
    $('li.active > a').parent().removeClass('active');
    $link.parent('li').addClass('active');
  }

  function initialize_js () {
    /* Materialize */
    // Parallax.
    $('.parallax').parallax();
    // Slider.
    $('.carousel.carousel-slider').carousel({full_width: true});

    /* Infinite scroll */
    $('.infinite-scroll:visible').jscroll({
      loadingHtml: '<span>Loading...</span>',
      padding: 50,
      nextSelector: 'a.jscroll-next',
      pagingSelector: '.pagination',
      debug: true
    });
  }

  $('body').addClass('js');

  /* Process ajax links */
  $(document).on('click', 'a.ajax-link', function(event) {
    event.preventDefault();
    if (!$(this).parent('li').hasClass("active")) {
      var $link = $(this);
      $.ajax({
        url: $link.attr("href") != '/' ? '/ajax' + $link.attr("href") : '/ajax',
        dataType: 'html',
      })
      .done(function(data) {
        $('#content').html(data);
        initialize_js();
        set_active_link($link.attr("href"));
        $(".modal-backdrop.in").remove();
        history.pushState({content: data}, null, $link.attr("href"));
      })
      .fail(function() {
        window.location.replace($link.attr("href"));
      });
    }
  });

  /* Back button */
  $(window).on("popstate", function(event) {
    if (event.originalEvent.state.content !== null) {
      $('#content').html(event.originalEvent.state.content);
      initialize_js();
      set_active_link (window.location.pathname);
    }
  });

  initialize_js();
});
