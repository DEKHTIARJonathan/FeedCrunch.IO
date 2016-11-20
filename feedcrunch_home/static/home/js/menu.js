; (function () {
	'use strict';

	var rgen = {};
	var package_ver = 'v1.13';


	/* HELPERS
	********************************************/
	rgen.spinner = function (el, cssclass) {
		'use strict';
		$("#page").css({ opacity: 0 });

		var cls = cssclass ? cssclass : '';
		if (el != "body") {
			if (!$(el).hasClass('pos-rel')) {
				$(el).addClass('pos-rel');
			}
		}
		$(el).prepend('<div class="spinner-wrp ' + cls + '"><div class="spinner"></div></div>');

	}
	if ($('html').attr('data-pageloader') === 'y') {

		if ($('html').attr('data-loadercls')) {
			rgen.spinner('body', $('html').attr('data-loadercls'));
		} else {
			rgen.spinner('body');
		}

		jQuery(window).load(function () {
			$('body > .spinner-wrp').fadeOut('slow', function () {
				$(this).remove();
				$("#page").animate({ opacity: 1 }, 500, function () { });
			});
		});
	}

	rgen.dmod = false;

	rgen.elcheck = function (el) {
		'use strict';
		if ($(el).length > 0) {
			return true;
		} else {
			return false;
		};
	}

	rgen.window = $(window);
	rgen.viewcheck = function (obj) {
		'use strict';

		rgen.animation_elements = $(obj);
		var window_height = rgen.window.height();
		var window_top_position = rgen.window.scrollTop();
		var window_bottom_position = (window_top_position + window_height);

		for (var i = 0; i < rgen.animation_elements.length; i++) {
			rgen.animation_elements[i]

			var $element = $(rgen.animation_elements[i]);
			var element_height = $element.outerHeight();
			var element_top_position = $element.offset().top;
			var element_bottom_position = (element_top_position + element_height);

			//check to see if this current container is within viewport
			if ((element_bottom_position >= window_top_position) && (element_top_position <= window_bottom_position)) {
				$element.addClass('in-view');
			} else {
				$element.removeClass('in-view');
			}
		}
	}

	rgen.uid = function () {
		'use strict';
		var uid = "";
		var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
		for (var i = 0; i < 3; i++)
			uid += possible.charAt(Math.floor(Math.random() * possible.length));
		return 'rg' + uid;
		//return ("0000" + (Math.random()*Math.pow(36,4) << 0).toString(36)).slice(-4);
	}

	rgen.demo = function () { if (rgen.dmod) { return rgenNotice(); } else { return true; }; }

	rgen.setId = function (obj, prefix, n) {
		'use strict';

		n++;
		var a = prefix + n;
		$(obj).css({ opacity: 0 });
		$(obj).attr("id", a);
		$(obj).addClass(a);

		// Accordion setup
		if ($(obj).is(".accordion-widget")) {
			$(obj).find(".acc-block").each(function (index, el) {
				var id = a + "-acc-block-" + index;
				$(this).find(".acc-hd").attr("data-accid", "#" + id);
				$(this).find(".acc-content").attr("id", id);
				$(this).find(".acc-hd").append('<i class="acc-open ' + $(obj).attr("data-acc-openclass") + ' "></i><i class="acc-close ' + $(obj).attr("data-acc-closeclass") + '"></i>');
			});
		}
	}

	rgen.mobmenu = function (el) {
		'use strict';

		$(el).on("click", function (e) {
			var nav = $(this).attr('data-nav');
			var c = $(this).attr('data-navclose');
			var o = $(this).attr('data-navopen');
			if ($(nav).hasClass('open')) {
				$(nav).removeClass('open');
				//$(this).find('i').removeClass($(this).attr('data-navclose')).addClass($(this).attr('data-navopen'));
				$(this).find('i').removeClass(c).addClass(o);
			} else {
				$(nav).addClass('open m-nav');
				//$(this).find('i').removeClass($(this).attr('data-navopen')).addClass($(this).attr('data-navclose'));

				$(this).find('i').removeClass(o).addClass(c);
			};
		});

	}

	rgen.getvar = function (v, default_v, val_type) {
		'use strict';
		if (val_type == 'n') {
			return v ? parseInt(v, 10) : default_v;
		}
		if (val_type == 'b') {
			if (v == 'true') { return true; }
			else if (v == 'false') { return false; }
			else { return default_v; }
		}
		if (val_type == 's') {
			if (v == 'false') {
				return false;
			} else {
				return v ? v : default_v;
			};

		}
	}

	jQuery(document).ready(function ($) {

		var $o = {};
		$o.r = !rgen.demo ? false : rgen.demo();
		$o.tooltip = $o.r ? $('[data-toggle="tooltip"]') : false;
		$o.navwrp = $('.nav-wrp').length > 0 && $o.r ? $('.nav-wrp') : false;
		$o.navlink = $('.nav-wrp').find(".nav-links").length > 0 && $o.r ? $o.navwrp.find(".nav-links") : false;

		$o.tooltip.tooltip({
			container: 'body'
		});


		/* RESPONSIVE
		********************************************/
		enquire.register("screen and (min-width: 992px)", {
			match : function() {
				rgen.device = 'd';
			},
			unmatch : function() { }
		}).register("(min-width: 200px) and (max-width: 991px)", {
			match : function() {
				rgen.device = 'm';
				$('.nav-transparent').removeClass('nav-transparent');
				$(".nav-wrp").removeClass('show-above').removeClass('bg-glass');
			},
			unmatch : function() {
				$('.nav-wrp').attr('data-glass') === 'y' ? $('.nav-wrp').addClass('bg-glass') : null;
				$('.nav-wrp').attr('data-above') === 'y' ? $('.nav-wrp').addClass('show-above') : null;
			}
		});


		/* NAVIGATION
		********************************************/
		if ($o.navlink) {
			rgen.mobmenu('.nav-handle');
			$o.navlink.find('a').smoothScroll({
				speed: 1200,
				offset: $o.navwrp.attr('data-sticky') == 'y' || $o.navwrp.attr('data-sticky-scroll') == 'y' ? -($o.navwrp.height() - 20) : 0,
				beforeScroll: function () {
					$o.navlink.find('a').removeClass('active');
					$('.nav-handle').trigger('tap');
				},
				afterScroll: function () {
					$(this).addClass('active');
				}
			});
		} else {
			rgen.mobmenu('.nav-handle');
		};

		/* LINK SCROLL
		********************************************/
		if (rgen.elcheck("#page[data-linkscroll='y']")) {
			rgen.linkscroll('a[href^="#"]:not(.nav-links)');
		};

		/* All navigation utilities
		********************************************/
		if ($o.navwrp) {

			var $nav = $o.navwrp;

			$nav.attr('data-glass') === 'y' ? $nav.addClass('bg-glass') : null;
			$nav.attr('data-above') === 'y' ? $nav.addClass('show-above') : null;

			if ($nav.attr('data-sticky') == 'y') {
				$nav.addClass('navbar-fixed-top').removeClass('show-above');
				$(window).scroll(function () {
					if ($(window).scrollTop() > $("nav").height()) {
						$nav.addClass("nav-sticky");
						$nav.attr('data-glass') === 'y' ? $nav.removeClass('bg-glass') : null;

					} else {
						$nav.removeClass("nav-sticky");
						$nav.attr('data-glass') === 'y' ? $nav.addClass('bg-glass') : null;
					}
				});
			};

			if ($nav.attr('data-sticky-scroll') == 'y') {
				$(window).scroll(function () {
					if ($(window).scrollTop() > $nav.height()) {
						$nav.addClass('navbar-fixed-top').addClass("nav-sticky");
					} else {
						$nav.removeClass('navbar-fixed-top').removeClass("nav-sticky");
					}
				});
			}

			if ($nav.attr('data-hide') == 'y') {
				$nav.addClass('nav-hide');
				$(window).scroll(function () {
					if ($(window).scrollTop() > $("nav").height()) {
						$nav.addClass("nav-show");
					} else {
						$nav.removeClass("nav-show");
					}
				});
			};

			$('ul.sf-menu').superfish({
				onShow: function () {
					// keep off screen momentarily
					$(this).css('top', '-1000px');

					// calculate position of submenu
					var winWidth = $(window).width();
					var outerWidth = $(this).outerWidth();
					var rightEdge = $(this).offset().left + outerWidth;

					// if difference is greater than zero, then add class to menu item
					if (rightEdge > winWidth) {
						$(this).addClass('right');
					}

					// remove top value so menu appears
					$(this).css('top', '');
				},
				onHide: function () {
					$(this).removeClass('right');
				}
			});
		}

		

	});

})();
