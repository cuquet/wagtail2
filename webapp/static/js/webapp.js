var window_height;
var scroll_distance;

// https://tempusdominus.github.io/bootstrap-4/Options/
$.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default, {
            icons: {
                time: 'mel-clock',
                date: 'mel-calendar',
                up: 'mel-angle-up',
                down: 'mel-angle-down',
                previous: 'mel-angle-left',
                next: 'mel-angle-right',
                today: 'mel-calendar-tick',
                clear: 'mel-trash',
                close: 'mel-cancel'
            },
            tooltips: {
                today: gettext('Go to today'),
                clear: gettext('Clear selection'),
                close: gettext('Close the picker'),
                selectMonth: gettext('Select Month'),
                prevMonth: gettext('Previous Month'),
                nextMonth: gettext('Next Month'),
                selectYear: gettext('Select Year'),
                prevYear: gettext('Previous Year'),
                nextYear: gettext('Next Year'),
                selectDecade: gettext('Select Decade'),
                prevDecade: gettext('Previous Decade'),
                nextDecade: gettext('Next Decade'),
                prevCentury: gettext('Previous Century'),
                nextCentury: gettext('Next Century'),
                incrementHour: gettext('Increment Hour'),
                pickHour: gettext('Pick Hour'),
                decrementHour:'Decrement Hour',
                incrementMinute: gettext('Increment Minute'),
                pickMinute: gettext('Pick Minute'),
                decrementMinute: gettext('Decrement Minute'),
                incrementSecond: gettext('Increment Second'),
                pickSecond: gettext('Pick Second'),
                decrementSecond: gettext('Decrement Second')
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
        LAUNCH.initParallax();
    }
});
// $(window).focus(function(){LAUNCH.backgroundResize();});


$(function () {
    "use strict";
    $(window).scroll(function(){
        LAUNCH.initParallax();
    });

    window_height = $(window).height();
    window.addEventListener('keydown', handleFirstTab);

    LAUNCH.initScrollTop();

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


    // ----efecte de color a navbar en avançar
    var $navbar = $('.navbar[color-on-scroll]');
    scroll_distance = $navbar.attr('color-on-scroll') || 300;
    if ($('.navbar-color-on-scroll').length != 0) {
        $(window).on('scroll', LAUNCH.checkScrollForTransparentNav);
    }
    LAUNCH.checkScrollForTransparentNav();
    LAUNCH.initNavSearch();
    LAUNCH.initAlertAutoDismiss();
    LAUNCH.backgroundResize();
    // LAUNCH.initParallax();
    // ----Parallax detect touch
    if("ontouchstart" in window){
        document.documentElement.className = document.documentElement.className + " touch";
    }
    if(!$("html").hasClass("touch")){
        // background fix
        $(".parallax").css("background-attachment", "fixed");
        LAUNCH.initParallax();
    }
});

LAUNCH = {
    misc: {
        transparent: true,
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

    initAlertAutoDismiss: function () {
        $('.alert[data-auto-dismiss]').each(function (index, element) {
            var $element = $(element),
                timeout = $element.data('auto-dismiss') || 5000;

            setTimeout(function () {
                $element.alert('close');
            }, timeout);
        });
    },

    initParallax: function () {
        var scrollTop = $(window).scrollTop();
        var oVal = (scrollTop / 3);
        $('.parallax-image').each(function() {
            $(this).css({
                'transform': 'translate3d(0,' + oVal + 'px,0)',
                '-webkit-transform': 'translate3d(0,' + oVal + 'px,0)',
                '-ms-transform': 'translate3d(0,' + oVal + 'px,0)',
                '-o-transform': 'translate3d(0,' + oVal + 'px,0)'
            });
        });

    },

    checkScrollForTransparentNav: debounce(function() {
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

    initNavSearch: function(){
        var search = document.getElementById('search'),
            searchWrapper = document.getElementById('search-wrapper'),
            closeIcon = document.getElementById('close-icon');
        if (search){
            search.onfocus = function () {
                searchWrapper.classList.add('search-expanded');
                this.addEventListener('transitionend', function () {
                    closeIcon.style.display = 'block';
                });
            },
            search.onblur = function () {
                searchWrapper.classList.remove('search-expanded');
                closeIcon.classList.add('closing');
                this.addEventListener('transitionend', function () {
                    closeIcon.classList.remove('closing');
                    closeIcon.style.display = 'none';
                });
            },
            closeIcon.onclick = function () {
                this.classList.add('closing');
                document.activeElement.blur();
                setTimeout(function () {
                    closeIcon.classList.remove('closing');
                }, 1000);
            }
        }
    },

    initScrollTop: function(){
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
            $(this).tooltip('hide');
        });
    },

    backgroundResize: function(){
        var windowH = window_height;
        $('.background').each(function(){
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
    }
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
}

function handleFirstTab(e) {
    if (e.keyCode === 9) { // the "I am a keyboard user" key
        document.body.classList.add('user-is-tabbing');
        window.removeEventListener('keydown', handleFirstTab);
    }
}

function simpleParallax(intensity, element) {
    $(window).scroll(function() {
        var scrollTop = $(window).scrollTop();
        var imgPos = scrollTop / intensity + 'px';
        element.css({
            'transform': 'translateY(' + imgPos + ')',
            '-webkit-transform': 'translateY(' + imgPos + ')',
            '-ms-transform': 'translateY(' + imgPos + ')',
            '-o-transform': 'translateY(' + imgPos + ')'
        });
    });
}