var window_height,
    searchVisible = 0,
    $navbar,
    scroll_distance;

$(function () {
    // PreLoader
    "use strict";
    // Scroll to the top
    // Check to see if the window is top if not then display button
    $('.scrollToTop').hide();
    $(window).scroll(function(){
        if ($(this).scrollTop() > 30) {
            $('.scrollToTop').show().removeClass('animated rollOut').addClass('animated rollIn'); //.fadeIn();
        } else {
            $('.scrollToTop').removeClass('animated rollIn').addClass('animated rollOut'); //.fadeOut();
        }
    });
    // Click event to scroll to top
    $('.scrollToTop').on('click', function(event) {
        event.preventDefault();
        $('html, body, div.main').animate({scrollTop : 0},800);
    });
    //  Activate the Tooltips
    $('[data-toggle="tooltip"], [rel="tooltip"]').tooltip();
    // Activate Popovers
    $('[data-toggle="popover"]').popover();
    // Navbar transitions and effects
    $('[data-target="#navbarCollapse"]').on('click', function () {
        $('body').toggleClass('nav-open');
    });
    $('#navbarCollapse').on('hidden.bs.collapse', function () {
        $('body').removeClass('nav-open');
        $('#bodyClick').remove();
    });
    $('#navbarCollapse').on('shown.bs.collapse', function () {
        var $this = $(this);
        var div = '<div id="bodyClick"></div>';
        $(div).appendTo('body').click(function() {
            $('body').removeClass('nav-open');
            $this.collapse('hide');
        })
    });
    // You can just turn off the transform placement on Popper
    // to make it only use top/left for positioning instead.
    // Then you can use transform for any animations/transitions
    // as you wish.
    // https://github.com/twbs/bootstrap/issues/23378
    Popper.Defaults.modifiers.computeStyle.gpuAcceleration = false;

    window_height = $(window).height();
    window.addEventListener('keydown', handleFirstTab);

    // efecte de color a navbar en avançar
    $navbar = $('.navbar[color-on-scroll]');
    scroll_distance = $navbar.attr('color-on-scroll') || 300;
    if ($('.navbar-color-on-scroll').length != 0) {
        $(window).on('scroll', LAUNCH.checkScrollForTransparentNavbar);
    }
    LAUNCH.checkScrollForTransparentNavbar();
    LAUNCH.initNavbarSearch();
    LAUNCH.AlertAutoDismiss();
    LAUNCH.backgroundResize();
    LAUNCH.ParallaxPosition();
    // Parallax
    // detect touch
    if("ontouchstart" in window){
        document.documentElement.className = document.documentElement.className + " touch";
    }
    if(!$("html").hasClass("touch")){
        // background fix
        $(".parallax").css("background-attachment", "fixed");
        LAUNCH.ParallaxPosition();
    }
});

// PreLoader
$(window).on("load", function () {
    setTimeout(function() {
        $('#preload').delay(2000).fadeOut(1000); //.addClass('animated fadeOutUp'); //
    });
});
$(window).on('resize', function() {
    LAUNCH.backgroundResize();
    if(!$("html").hasClass("touch")){
        LAUNCH.ParallaxPosition();
    }
});
$(window).scroll(function(){LAUNCH.ParallaxPosition();});
// $(window).focus(function(){LAUNCH.backgroundResize();});


LAUNCH = {
    misc: {
        transparent: true,
    },

    ButtonScrollUp: function () {
        $(".btn-scrolldown").click(function (event) {
            var lng_scroll;
            if (responsive >= 768) {
                lng_scroll = '+=700px';
            } else {
                lng_scroll = '+=600px';
            }
            $('html, body').animate({scrollTop: lng_scroll}, 800);
        });
    },

    Selectlanguage: function (action, csrf) {
        //Language selector on navbar top ul->li
        $("#language-list a").click(function () {
            var form = $(document.createElement('form'));
            $(form).attr('action', action);
            $(form).attr('method', 'POST');
            var input = $("<input>").attr("type", "hidden").attr("name", "language").val($(this).attr('rel'));
            $(form).append($(input));
            var input = $("<input>").attr("type", "hidden").attr("name", "csrfmiddlewaretoken").val(csrf);
            $(form).append($(input));
            $(form).appendTo(document.body).submit();
        });
        if ($('#language_selector_form').length) {
            $('#language_selector_form').on('change', function () {
                this.submit();
            });
            $('#language_selector_form > input').hide();
        }
    },

    ModalSubmit: function () {
        // https://gist.github.com/havvg/3226804
        $('.modal').on('submit', 'form[data-async]', function (e) {
            var $form = $(this);
            var $target = $($form.attr('data-target'));
            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: $form.serializeArray(),
                success: function (data, status) {
                    $target.html(data);
                    setTimeout(function () {
                        $(".modal").modal('hide');
                    }, 8000);
                }
            });
            event.preventDefault();
        });
        $('.modal').on("click", 'input[type="submit"], button[type="submit"]', function () {
            $('form[data-async] input[type=submit], form[data-async] button[type=submit]', $(this).parents("form")).removeAttr("clicked");
            $(this).attr("clicked", "true");
        });
    },

    AlertAutoDismiss: function () {
        $('.alert[data-auto-dismiss]').each(function (index, element) {
            var $element = $(element),
                timeout = $element.data('auto-dismiss') || 5000;

            setTimeout(function () {
                $element.alert('close');
            }, timeout);
        });
    },

    ParallaxPosition: debounce(function () {
        var current_scroll = $(this).scrollTop();

        oVal = ($(window).scrollTop() / 3);
        $(".parallax-image").each(function(i) {
            $(this).css({
                'transform': 'translate3d(0,' + oVal + 'px,0)',
                '-webkit-transform': 'translate3d(0,' + oVal + 'px,0)',
                '-ms-transform': 'translate3d(0,' + oVal + 'px,0)',
                '-o-transform': 'translate3d(0,' + oVal + 'px,0)'
            });
        });

    }, 6),

    /*ParallaxPosition: function(e){
        var heightWindow = window_height;
        var topWindow = $(window).scrollTop();
        var bottomWindow = topWindow + heightWindow;
        var currentWindow = (topWindow + bottomWindow) / 2;
        $(".parallax-image").each(function(i){
            var path = $(this);
            var height = path.height();
            var top = path.offset().top;
            var bottom = top + height;
            // only when in range
            if(bottomWindow > top && topWindow < bottom){
                var imgW = path.data("resized-imgW");
                var imgH = path.data("resized-imgH");
                // min when image touch top of window
                var min = 0;
                // max when image touch bottom of window
                var max = - imgH + heightWindow;
                // overflow changes parallax
                var overflowH = height < heightWindow ? imgH - height : imgH - heightWindow; // fix height on overflow
                top = top - overflowH;
                bottom = bottom + overflowH;
                // value with linear interpolation
                var value = min + (max - min) * (currentWindow - top) / (bottom - top);
                // set background-position
                var orizontalPosition = path.attr("data-oriz-pos");
                orizontalPosition = orizontalPosition ? orizontalPosition : "50%";
                $(this).css("background-position", orizontalPosition + " " + value + "px");
            }
        });
    },*/

    /*    NavbarBurguerImage: function() {
        var $navbar = $('.navbar').find('.navbar-translate').siblings('.navbar-collapse');
        var background_image = $navbar.data('nav-image');

        if ($(window).width() < 991 || $('body').hasClass('burger-menu')) {
            if (background_image != undefined) {
                $navbar.css('background', "url('" + background_image + "')")
                    .removeAttr('data-nav-image')
                    .css('background-size', "cover")
                    .addClass('has-image');
            }
        } else if (background_image != undefined) {
            $navbar.css('background', "")
                .attr('data-nav-image', '' + background_image + '')
                .css('background-size', "")
                .removeClass('has-image');
        }
    },*/

    checkScrollForTransparentNavbar: debounce(function() {
        if ($(document).scrollTop() > scroll_distance) {
          if (LAUNCH.misc.transparent) {
            LAUNCH.misc.transparent = false;
            $('.navbar-color-on-scroll').removeClass('navbar-transparent');
          }
        } else {
          if (!LAUNCH.misc.transparent) {
            LAUNCH.misc.transparent = true;
            $('.navbar-color-on-scroll').addClass('navbar-transparent');
          }
        }
     }, 17),

    initNavbarSearch: function(){
        $('[data-toggle="search"]').click(function(){
            if(searchVisible == 0){
                searchVisible = 1;
                $(this).parent().addClass('active');
                $('.navbar-search-form').animate({width: 'toggle'}, { complete: function() {
                        $('.navbar-search-form input').focus();
                    },
                });
            } else {
                searchVisible = 0;
                $(this).parent().removeClass('active');
                $(this).blur();
                $('.navbar-search-form').animate({width: 'toggle'}, { complete: function() {
                        $('.navbar-search-form input').blur();
                    },
                });
            }
        });
    },

    backgroundResize: function(){
        var windowH = window_height;
        $(".background").each(function(i){
            var path = $(this);
            // variables
            var contW = path.width();
            var contH = path.height();
            var imgW = path.attr("data-img-width");
            var imgH = path.attr("data-img-height");
            var ratio = imgW / imgH;
            // overflowing difference
            var diff = parseFloat(path.attr("data-diff"));
            diff = diff ? diff : 0;
            // remaining height to have fullscreen image only on parallax
            var remainingH = 0;
            if(path.hasClass("parallax-image") && !$("html").hasClass("touch")){
                var maxH = contH > windowH ? contH : windowH;
                remainingH = windowH - contH;
            }
            // set img values depending on cont
            imgH = contH + remainingH + diff;
            imgW = imgH * ratio;
            // fix when too large
            if(contW > imgW){
                imgW = contW;
                imgH = imgW / ratio;
            }
            //
            path.data("resized-imgW", imgW);
            path.data("resized-imgH", imgH);
            path.css("background-size", imgW + "px " + imgH + "px");
        });
    },

    DatePicker: function(){
        $('.datepicker').datepicker({
            weekStart:1,
            format: 'dd/mm/yyyy',
            color: 'green',
        });
    },
};


// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this,
      args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    }, wait);
    if (immediate && !timeout) func.apply(context, args);
  };
};

function handleFirstTab(e) {
    if (e.keyCode === 9) { // the "I am a keyboard user" key
        document.body.classList.add('user-is-tabbing');
        window.removeEventListener('keydown', handleFirstTab);
    }
};
