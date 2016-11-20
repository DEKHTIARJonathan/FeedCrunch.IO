/*
++++++++++++++++++++++++++++++++++++++++++++++++++++++
AUTHOR : R_GENESIS
PROJECT : AppLead - App Landing Pages
This file licensed to R_GENESIS (http://themeforest.net/user/r_genesis) and it’s strictly prohibited to copy or reuse it.
Copyright 2015-2016 R.Genesis.Art
++++++++++++++++++++++++++++++++++++++++++++++++++++++
*/
; (function () {
	'use strict';

	var rgen = {};
	var package_ver = 'v1.13';

	/* CONFIG
	********************************************/
	rgen.config = {
		/*
		TWITTER
		String: consumer key. make sure to have your app read-only
		String: consumer secret key. make sure to have your app read-only
		*********************/
		twitter: {
			consumer_key: 'YOUR_CONSUMER_KEY',
			consumer_secret: 'YOUR_CONSUMER_SECRET_KEY'
		},

		/*
		URL OF SUCCESS PAGE ON FORM SUBMIT
		*********************/
		success_url: "thankyou.html"
	}


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


	rgen.parallax = function (obj, type) {
		'use strict';

		// create variables
		var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

		// on window scroll event
		rgen.window.on('scroll resize', function () {
			scrollTop = window.pageYOffset || document.documentElement.scrollTop;
		});


		// for each of content parallax element
		if (type == 'element') {
			var $contentObj = $(obj);
			var fgOffset = parseInt($contentObj.offset().top, 10);
			var yPos;
			var speed = $contentObj.attr('data-speed') ? parseInt($contentObj.attr('data-speed'), 10) : 4;

			$contentObj.parent().css({ overflow: 'hidden' });

			rgen.window.on('scroll resize', function () {
				rgen.viewcheck($contentObj);
				if ($contentObj.hasClass('in-view')) {
					yPos = ((scrollTop - fgOffset) / speed);
					$contentObj.css('transform', 'translate3d(0px, ' + yPos + 'px, ' + '0)');
				}
			});
		}

		if (type == 'background') {
			var $backgroundObj = $(obj);
			var bgOffset = parseInt($backgroundObj.offset().top, 10);
			var yPos;
			var coords;
			var speed = ($backgroundObj.data('speed') || 0);

			rgen.window.on('scroll resize', function () {
				yPos = - ((scrollTop - bgOffset) / speed);
				coords = 'center ' + yPos + 'px';
				$backgroundObj.css({ backgroundPosition: coords });
			});
		}
		// triggers winodw scroll for refresh
		rgen.window.trigger('scroll');
	};


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

	rgen.getMultiScripts = function (arr, path) {
		'use strict';

		var _arr = $.map(arr, function (scr) {
			return $.getScript((path || "") + scr);
		});

		_arr.push($.Deferred(function (deferred) {
			$(deferred.resolve);
		}));

		return $.when.apply($, _arr);
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

	rgen.owlitems = function (arr) {
		'use strict';
		if (typeof (arr) == "string" && arr != 'false') {
			var t1 = arr.split('|');
			var t2 = {};
			$.each(t1, function (index, val) {
				var str = val;
				var newarr = str.split(',');
				t2[newarr[0]] = {}
				t2[newarr[0]] = { items: parseInt(newarr[1], 10) };
			});
			return t2;
		} else if (arr === 'false') {
			return {};
		} else {
			return false;
		}
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

	rgen.slider = function (owlObj) {

		'use strict';

		var resObj = {
			0: { items: 1 },
			420: { items: 2 },
			600: { items: 3 },
			768: { items: 3 },
			980: { items: 4 }
		}

		var owlEle = $(owlObj + ' .owl-carousel'),
			o = $(owlObj);

		var config = {
			center: rgen.getvar(o.attr('data-center'), false, 'b'),
			stagePadding: rgen.getvar(o.attr('data-stpd'), 0, 'n'),
			items: rgen.getvar(o.attr('data-items'), 5, 'n'),
			margin: rgen.getvar(o.attr('data-margin'), 0, 'n'),
			nav: rgen.getvar(o.attr('data-nav'), false, 'b'),
			dots: rgen.getvar(o.attr('data-pager'), false, 'b'),
			slideby: rgen.getvar(o.attr('data-slideby'), 1, 'n'),
			rbase: rgen.getvar(o.attr('data-rbase'), o.parent(), 's'),
			res: o.attr('data-itemrange') ? rgen.owlitems(o.attr('data-itemrange')) : resObj,
			animOut: rgen.getvar(o.attr('data-out'), 'fadeOut', 's'),
			animIn: rgen.getvar(o.attr('data-in'), 'fadeIn', 's'),
			autoplay: rgen.getvar(o.attr('data-autoplay'), false, 'b'),
			autoplayTimeout: rgen.getvar(o.attr('data-timeout'), 3000, 'n'),
			autoplayHoverPause: rgen.getvar(o.attr('data-hstop'), true, 'b'),
			loop: rgen.getvar(o.attr('data-loop'), false, 'b'),
			autoWidth: rgen.getvar(o.attr('data-awidth'), false, 'b'),
			autoHeight: rgen.getvar(o.attr('data-hauto'), true, 'b'),
			touchDrag: rgen.getvar(o.attr('data-tdrag'), true, 'b'),
			mouseDrag: rgen.getvar(o.attr('data-mdrag'), true, 'b'),
			pullDrag: rgen.getvar(o.attr('data-pdrag'), true, 'b'),
			contentHeight: rgen.getvar(o.attr('data-h'), true, 'b')
		}
		o.animate({ opacity: 1 }, 300, function () {

			if (owlEle.find(".owl-stage").length === 0) {
				owlEle.owlCarousel({
					center: config.center,
					stagePadding: config.stagePadding,
					items: config.items,
					margin: config.margin,
					nav: config.nav,
					dots: config.dots,
					slideBy: config.slideby,
					navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
					responsiveBaseElement: config.rbase,
					responsive: config.res,
					loop: $(owlObj + " .owl-carousel > .item").length > 1 ? config.loop : false,
					animateOut: config.animOut, //'slideOutDown',
					animateIn: config.animIn, //'flipInX',
					autoplay: config.autoplay,
					autoplayTimeout: config.autoplayTimeout,
					autoplayHoverPause: config.autoplayHoverPause,
					autoHeight: config.autoHeight,
					autoWidth: config.autoWidth,
					touchDrag: config.touchDrag,
					mouseDrag: config.mouseDrag,
					pullDrag: config.pullDrag,
					autoplaySpeed: 2000,

					onInitialized: function () {
						owlEle.animate({ opacity: 1 }, 300);
						
						// Align arrows
						owlEle.find('.owl-nav').css({
							top: owlEle.find('.owl-stage-outer').outerHeight() / 2
						});
						rgen.blazyload(owlEle);
					}
				});

				o.find('.carousel-btn .prev').on('click', function () { owlEle.trigger('prev.owl.carousel'); });
				o.find('.carousel-btn .next').on('click', function () { owlEle.trigger('next.owl.carousel'); });
			}
		});
	}

	rgen.fullwh = function (obj) {
		'use strict';
		// global vars
		var winWidth = $(window).width();
		var winHeight = $(window).height();
		// set initial div height / width
		$(obj).css({
			'width': winWidth,
			'height': winHeight,
		});
	}
	rgen.fullh = function (obj, wrp) {
		'use strict';

		if (wrp) {
			var winHeight = $(obj).closest(wrp).height();
		} else {
			var winHeight = $(window).height();
		}

		// set initial div height / width
		$(obj).css({
			'height': winHeight,
		});
	}


	rgen.swiper_slider = function (obj) {

		'use strict';

		var config = {
			autoplay: rgen.getvar($(obj).attr('data-autoplay'), 1000, 'n'),
			speed: rgen.getvar($(obj).attr('data-speed'), 1000, 'n'),
			fullsize: rgen.getvar($(obj).attr('data-fullsize'), false, 'b'),
		}

		if (config.fullsize) {
			rgen.fullwh(obj);
			$(window).resize(function () {
				rgen.fullwh(obj);
			});
		};

		var swiper = new Swiper(obj, {

			direction: 'horizontal',
			touchEventsTarget: 'container',
			speed: config.speed,
			autoplay: config.autoplay,
			autoplayDisableOnInteraction: true,
			effect: 'fade', // 'slide' or 'fade' or 'cube' or 'coverflow'
			parallax: false,
			pagination: obj + ' .swiper-pagination',
			paginationClickable: true,
			nextButton: obj + ' .swiper-button-next',
			prevButton: obj + ' .swiper-button-prev',
			onInit: function (swiper) {
				$(obj).animate({ opacity: 1 }, 300);
			}
		});
	}

	rgen.swiper_gallery = function (obj) {
		'use strict';

		var galleryTop = new Swiper(obj + ' .gallery-top', {
			nextButton: obj + ' .swiper-button-next',
			prevButton: obj + ' .swiper-button-prev',
			spaceBetween: 0,
			onInit: function (swiper) {
				$(obj).animate({ opacity: 1 }, 300);
			},
			preloadImages: false,
			lazyLoading: true
		});
		var galleryThumbs = new Swiper(obj + ' .gallery-thumbs', {
			spaceBetween: 10,
			centeredSlides: true,
			slidesPerView: 'auto',
			touchRatio: 0.2,
			slideToClickedSlide: true,
			preloadImages: false,
			lazyLoading: true
		});
		galleryTop.params.control = galleryThumbs;
		galleryThumbs.params.control = galleryTop;
	}


	rgen.tabs = function (obj) {
		'use strict';

		if ($(obj.tb).hasClass('tabs-auto')) {
			var t = 0,
				tb_activeClass = $(obj.tb).attr('data-tb-active') ? 'active '+$(obj.tb).attr('data-tb-active') : 'active',
				pn_activeClass = $(obj.tb).attr('data-pn-active') ? 'active '+$(obj.tb).attr('data-pn-active') : 'active';

			$(obj.tb).find('.tb-list > .tb').each(function () {
				var tb = obj.count + '-tb-' + t;
				$(this).attr("data-tb", '#' + tb);
				$(obj.tb).find('.tb-content > .tb-pn:eq(' + t + ')').attr("id", tb);
				t++;
			});

			$(obj.tb).on('click', '.tb-list > .tb', function (e) {
				e.preventDefault();

				$(this).closest('.tb-list').find('.tb').removeClass(tb_activeClass);
				$(this).addClass(tb_activeClass);

				var target = $($(this).attr('data-tb'));
				target.siblings('.tb-pn').removeClass(pn_activeClass);
				target.addClass(pn_activeClass);

			});
			if ($(obj.tb).find('.tb-list > .tb').hasClass(tb_activeClass)) {
				$(obj.tb).find('.tb-list > .tb.active').click();
			} else {
				$(obj.tb).find('.tb-list > .tb:first').click();
			};

		} else {
			$('[data-tb]').each(function (index, el) {
				var target = $(this).attr('data-tb');
				$(target).addClass('tab-pn');
			});
			$(obj).on('click', function (e) {
				e.preventDefault();

				$(obj).closest('.tab-widget').find('[data-tb]').removeClass('active');
				$(this).addClass('active');

				var target = $($(this).attr('data-tb'));
				target.siblings('.tab-pn').hide();
				target.show().addClass('active');

			}).eq(0).click();
		};

	}

	rgen.accordion = function (obj) {
		'use strict';

		function close_acc(parent_obj) {
			$(parent_obj).find('.acc-hd').removeClass('active');
			$(parent_obj).find('.acc-content').stop().slideUp(200).removeClass('open');
		}

		$(obj).animate({ opacity: 1 }, 500, function () { });

		$(obj).on('click', '.acc-hd', function (e) {
			e.stopPropagation();
			e.preventDefault();

			var content = $(this).attr('data-accid');
			if ($(this).is('.active')) {
				close_acc(obj);
			} else {
				close_acc(obj);

				// Add active class to section title
				$(this).addClass('active');
				// Open up the hidden content panel
				$(obj).find(content).stop().slideDown(200).addClass('open');
			}

		});

		// First open option
		if ($(obj).attr("data-acc-firstopen") == 'y') {
			$(obj).find(".acc-block:first .acc-hd").click();
		} else {
			close_acc(obj);
		}

	}

	rgen.global_validation = {
		form: '',
		rules: {
			email: { required: true, email: true },
			name: { required: true },
			message: { required: true },
			phone: { required: true, number: true },
			date: { required: true, date: true },
			datetime: { required: true, date: true },
		},
		msgpos: 'normal',
		msg: {
			email: { email: "Please, enter a valid email" }
		},
		subscribe_successMsg: "You are in list. We will inform you as soon as we finish.",
		form_successMsg: "Thank you for contact us. We will contact you as soon as possible.",

		successMsg: "",
		errorMsg: "Oops! Looks like something went wrong. Please try again later."
	}

	rgen.formVaidate = function (obj) {
		'use strict';
		var msgpos = $(obj.form).attr('data-msgpos') ? $(obj.form).attr('data-msgpos') : 'normal';
		if (msgpos == 'append') {
			$(obj.form).validate({
				onfocusout: false,
				onkeyup: false,
				rules: obj.rules,
				messages: obj.msg,
				highlight: false,
				errorPlacement: function (error, element) {
					if (msgpos == 'append') {
						error.appendTo(element.closest("form").find('.msg-wrp'));
					};
				},
				success: function (element) {
					element.remove();
				}
			});
		} else {
			$(obj.form).validate({
				onfocusout: false,
				onkeyup: false,
				rules: obj.rules,
				messages: obj.msg,
				highlight: false,
				success: function (element) {
					element.remove();
				}
			});
		};
	}

	rgen.resetForm = function (form) {
		'use strict';
		$(form).find('input[type="text"], input[type="email"], textarea').val(null);
	}

	rgen.contactForm = function ($form, formData, validate_data) {
		'use strict';

		if ($form.find('label.error').length > 0) { $form.find('label.error').hide(); }

		var $btn = $form.find(".btn").button('loading');
		var timer = 4000;

		if ($form.valid()) {
			$.ajax({
				url: $form.attr('action'),
				type: 'POST',
				data: formData,
				success: function (data) {
					if (data.status == 'error') {
						// Email subscription error messages
						swal("Error!", data.type, "error");
						$btn.button('reset');
						rgen.resetForm($form);
					} else {
						//swal("Success!", validate_data.successMsg, "success");
						swal({
							type: "success",
							title: "Success!",
							text: validate_data.successMsg,
							timer: timer
						}, function () {
							if ($form.attr('data-success-redirect') === 'y') {
								window.location = rgen.config.success_url;
							}
						});

						$btn.button('reset');
						$.magnificPopup.close();
						rgen.resetForm($form);

						setTimeout(function () { swal.close(); }, timer);
					};
				},
				error: function () {
					swal("Error!", validate_data.errorMsg, "error");
					$btn.button('reset');
					$.magnificPopup.close();
					setTimeout(function () { swal.close(); }, timer);
				}
			});
		} else {
			$form.find("label.error").delay(timer).fadeOut('400', function () {
				$(this).remove();
			});
			$btn.button('reset');
		};
	}

	rgen.formWidget = function (obj) {
		'use strict';

		var config = {
			popup_selector: $(obj).attr('data-popup') ? '.' + $(obj).attr('data-popup') : false,
			form_type: $(obj).attr('data-formtype') ? $(obj).attr('data-formtype') : 'normal',
			form_selector: obj
		}

		var $form = $(config.form_selector);

		// Validation rules
		rgen.global_validation.form = config.form_selector;
		var validate_data = rgen.global_validation;

		// Pop up form
		if (config.popup_selector) {
			$(config.popup_selector).each(function (index, el) {
				$(this).magnificPopup({
					type: 'inline',
					preloader: false
				});
			});
		};

		// Date and time picker options
		if ($form.find(".date-pick").length > 0 || $form.find(".datetime-pick").length > 0) {

			var date_script_arr = [
				/*
				http://www.malot.fr/bootstrap-datetimepicker/index.php
				https://github.com/smalot/bootstrap-datetimepicker
				*/
				"lib/bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js"
			];

			rgen.getMultiScripts(date_script_arr, '').done(function () {
				// Date picker
				if ($form.find(".date-pick").length > 0) {
					$form.find(".date-pick").each(function (index, el) {
						$(this).datetimepicker({
							autoclose: true,
							startView: 2,
							minView: 2
						});
					});
				};

				// Date time picker
				if ($form.find(".datetime-pick").length > 0) {
					$form.find(".datetime-pick").each(function (index, el) {
						$(this).datetimepicker({
							autoclose: true
						});
					});
				};
			});
		}
		

		// Form validation
		rgen.formVaidate(validate_data);

		// Form
		$form.find('button').off('click').on('click', function (e) {
			e.preventDefault();
			if (config.form_type == "newsletter") {
				rgen.global_validation.successMsg = rgen.global_validation.subscribe_successMsg;
			} else {
				rgen.global_validation.successMsg = rgen.global_validation.form_successMsg;
			};

			rgen.contactForm($form, $form.serializeObject(), validate_data);
			return false;
		});
	}

	$.fn.serializeObject = function () {
		'use strict';

		var o = {};
		var a = this.serializeArray();
		$.each(a, function () {

			// Field labels
			var field_label = $('[name=' + this.name + ']').attr('data-label') ? $('[name=' + this.name + ']').attr('data-label') : this.name;

			// Field values
			if (o[this.name]) {
				if (!o[this.name].push) {
					o[this.name] = [o[this.name]];
				}
				o[this.name].push({ val: this.value, label: field_label } || '');
			} else {
				//o[this.name] = this.value || '';
				o[this.name] = { val: this.value, label: field_label } || '';
			}
		});
		return o;
	};

	rgen.videoBg = function (obj, imglist) {
		'use strict';
		var isMobile = {
			Android: function () {
				return navigator.userAgent.match(/Android/i);
			},
			BlackBerry: function () {
				return navigator.userAgent.match(/BlackBerry/i);
			},
			iOS: function () {
				return navigator.userAgent.match(/iPhone|iPad|iPod/i);
			},
			Opera: function () {
				return navigator.userAgent.match(/Opera Mini/i);
			},
			Windows: function () {
				return navigator.userAgent.match(/IEMobile/i);
			},
			any: function () {
				return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
			}
		};

		if (isMobile.any()) {
			$(obj).css("display", "none");
			/*$(obj).vegas({
				slides: [
					{ src: "images/bg-1.jpg" },
					{ src: "images/bg-2.jpg" },
					{ src: "images/bg-3.jpg" },
					{ src: "images/bg-4.jpg" }
				]
				slides: imglist
			});*/
		}
		else {
			$(obj).css("display", "block");
			$(obj).YTPlayer({
				onReady: function (player) { }
			});
		}
	}
	rgen.videoPopup = function (obj) {
		'use strict';
		$(obj).magnificPopup({
			disableOn: 700,
			type: 'iframe',
			mainClass: 'mfp-fade',
			removalDelay: 160,
			preloader: false,

			fixedContentPos: false
		});
	};

	rgen.inlinePopup = function (obj) {
		'use strict';
		$('body').off('click').on('click', obj, function (e) {
			$(this).magnificPopup({
				type: 'inline',
				preloader: false
			}).click();
		});
	}

	rgen.bgSlider = function (setting) {
		'use strict';
		setTimeout(function () {
			$(setting.obj).vegas({
				delay: setting.delay,
				slides: setting.slides,
				animation: setting.effect
			});
		}, 1000);

	}

	rgen.linkscroll = function (obj) {
		'use strict';
		$(document).on('click', obj, function (e) {
			e.preventDefault();
			if ($(this).closest('.nav-links').hasClass('nav-links') == false && $(this).attr('href').indexOf("popup") === -1) {
				// target element id
				var id = $(this).attr('href');
				// target element
				var $id = $(id);
				if ($id.length === 0) { return; }
				// top position relative to the document
				var pos = $(id).offset().top;
				// animated top scrolling
				$('body, html').animate({ scrollTop: pos }, 1200);
			};
		});
	}

	rgen.countdown = function (obj) {
		'use strict';

		var o = $(obj);
		var config = {
			day: parseInt(o.attr("data-day"), 10),
			month: parseInt(o.attr("data-month"), 10),
			year: parseInt(o.attr("data-year"), 10),
			hour: parseInt(o.attr("data-hr"), 10),
			min: parseInt(o.attr("data-min"), 10),
			sec: parseInt(o.attr("data-sec"), 10)
		}

		var oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
		var firstDate = new Date(config.year, config.month - 1, config.day - 1);
		var d = new Date();
		var secondDate = new Date(d.getFullYear(), d.getMonth(), d.getDate());
		var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime()) / (oneDay)));

		var countdownHtml = '<div class="inner-dashboard">';
		countdownHtml += '	<!-- DAYS -->';
		countdownHtml += '	<div class="dash days_dash">';
		countdownHtml += '		<div class="inner-dash">';
		countdownHtml += diffDays > 99 ? '<div class="digit">0</div>' : '';
		//countdownHtml += '<div class="digit">0</div>';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '		</div>';
		countdownHtml += '		<span class="dash_title">days</span>';
		countdownHtml += '	</div>';
		countdownHtml += '	<!-- HOURS -->';
		countdownHtml += '	<div class="dash hours_dash">';
		countdownHtml += '		<div class="inner-dash">';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '		</div>';
		countdownHtml += '		<span class="dash_title">hours</span>';
		countdownHtml += '	</div>';
		countdownHtml += '	<!-- MINIUTES -->';
		countdownHtml += '	<div class="dash minutes_dash">';
		countdownHtml += '		<div class="inner-dash">';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '		</div>';
		countdownHtml += '		<span class="dash_title">minutes</span>';
		countdownHtml += '	</div>';
		countdownHtml += '	<!-- SECONDS -->';
		countdownHtml += '	<div class="dash seconds_dash">';
		countdownHtml += '		<div class="inner-dash">';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '			<div class="digit">0</div>';
		countdownHtml += '		</div>';
		countdownHtml += '		<span class="dash_title">seconds</span>';
		countdownHtml += '	</div>';
		countdownHtml += '</div>';

		o.html(countdownHtml);

		// DESKTOP CLOCK
		o.countDown({
			targetDate: {
				'day': config.day,
				'month': config.month,
				'year': config.year,
				'hour': config.hour,
				'min': config.min,
				'sec': config.sec
			},
			omitWeeks: true
		});
	}

	rgen.instagram = function (obj) {
		'use strict';

		var o = $(obj),
			id = o.attr('id');
		o.find('.feed-data').socialfeed({
			instagram: {
				accounts: ['*'],
				limit: o.attr('data-insta-limit') ? o.attr('data-insta-limit') : 8,
				userdata: o.attr('data-insta-user') ? o.attr('data-insta-user') : '',
				client_id: rgen.config.instagram.client_id,
				access_token: rgen.config.instagram.access_token,
				tpl_class: o.attr('data-insta-tplclass') ? o.attr('data-insta-tplclass') : '',
			},

			// GENERAL SETTINGS
			template: 'lib/social-feed/' + o.attr('data-insta-tpl') + '.html',
			length: o.attr('data-insta-length') ? parseInt(o.attr('data-insta-length'), 10) : 256,
			show_media: true,
			update_period: false,

			callback: function () {
				o.animate({ opacity: 1 }, 500, function () {
					if (rgen.elcheck('#' + id + ' .instagram-carousel')) {
						rgen.slider('#' + id + ' .instagram-carousel');
					}
				});
			}
		});
	}

	rgen.twitter = function (obj) {
		'use strict';

		var o = $(obj),
			id = o.attr('id');
		o.find('.feed-data').socialfeed({
			twitter: {
				accounts: ['@' + o.attr('data-twitter-user')],
				limit: o.attr('data-twitter-limit') ? o.attr('data-twitter-limit') : 6,
				consumer_key: rgen.config.twitter.consumer_key,
				consumer_secret: rgen.config.twitter.consumer_secret,
				tpl_class: o.attr('data-twitter-tplclass') ? o.attr('data-twitter-tplclass') : '',
				tpl_class1: o.attr('data-twitter-tplclass1') ? o.attr('data-twitter-tplclass1') : '',
				tpl_class2: o.attr('data-twitter-tplclass2') ? o.attr('data-twitter-tplclass2') : '',
				tpl_class3: o.attr('data-twitter-tplclass3') ? o.attr('data-twitter-tplclass3') : '',
				tpl_class4: o.attr('data-twitter-tplclass4') ? o.attr('data-twitter-tplclass4') : ''
			},

			// GENERAL SETTINGS
			template: 'lib/social-feed/' + o.attr('data-twitter-tpl') + '.html',
			length: o.attr('data-twitter-length') ? parseInt(o.attr('data-twitter-length'), 10) : 256,
			show_media: true,
			update_period: false,

			callback: function () {
				o.animate({ opacity: 1 }, 500, function () {
					if (rgen.elcheck('#' + id + ' .twitter-carousel')) {
						rgen.slider('#' + id + ' .twitter-carousel');
					}
				});
			}
		});
	}


	rgen.filter = function (obj) {
		'use strict';

		$(obj).animate({ opacity: 1 }, 500, function () { });
		var filterObj = $(obj);
		var container = filterObj.find('.filter-container');
		var list = filterObj.find('.filter-list');
		var time = 500;

		list.find('[data-filter]').on('click', function (event) {
			event.preventDefault();

			var filter = $(this).attr("data-filter");

			list.find("[data-filter]").removeClass('active');
			$(this).addClass('active');

			container.find('.filter-content').stop().animate({ opacity: 0 }, 150, function () {
				$(this).hide();
				if (filter == 'all') {
					container.find('.filter-content').show().stop().animate({ opacity: 1 }, time);
				} else {
					$(filter).show().stop().animate({ opacity: 1 }, time);
				}
			});

		});

		list.find('.active') ? list.find('.active').trigger('click') : list.find('[data-filter]').first().trigger('click');
	}

	rgen.gmapset = function (obj) {
		'use strict';

		var o = $(obj);
		o.css({ height: o.attr("data-map-height") });
		o.animate({ opacity: 1 }, 500, function () {
			o.mapit({
				latitude: o.attr("data-map-latitude"),
				longitude: o.attr("data-map-longitude"),
				zoom: 16,
				type: 'ROADMAP',
				scrollwheel: false,
				marker: {
					latitude: o.attr("data-map-latitude"),
					longitude: o.attr("data-map-longitude"),
					icon: 'images/gmap-marker.png',
					title: o.attr("data-map-markerhd"),
					open: false,
					center: true
				},
				address: o.attr("data-map-markerhtml"),
				styles: o.attr("data-map-styles") ? 'GRAYSCALE' : false //'GRAYSCALE',
			});
		});

	}

	rgen.vide = function (obj) {
		'use strict';

		var videofile = $(obj).attr("data-vide-src");
		$(obj).animate({ opacity: 1 }, 500, function () { });
		$(obj).vide({
			mp4: videofile,
			webm: videofile,
			ogv: videofile,
			poster: videofile + ".jpg"
		}, {
				volume: 1,
				playbackRate: 1,
				muted: true,
				loop: true,
				autoplay: true,
				position: 'center center', // Similar to the CSS `background-position` property.
				posterType: 'jpg', // Poster image type. "detect" — auto-detection; "none" — no poster; "jpg", "png", "gif",... - extensions.
				resizing: true, // Auto-resizing, read: https://github.com/VodkaBears/Vide#resizing
				bgColor: 'transparent', // Allow custom background-color for Vide div,
				className: '' // Add custom CSS class to Vide div
			});
	}

	rgen.blazyload = function (obj){
		'use strict';

		var bLazy = new Blazy({
			loadInvisible: true,
			success: function(ele){
				if ($(obj).hasClass('owl-carousel')) {
					$(obj).find('.owl-nav').css({
						top: $(obj).find('.owl-stage-outer').outerHeight() / 2
					});
				}
			}
	    });
	}

	$("#config_style").attr('href', 'css/configstyle.css?' + rgen.uid());


	jQuery(document).ready(function ($) {

		var $o = {};
		$o.r = !rgen.demo ? false : rgen.demo();
		$o.tooltip = $o.r ? $('[data-toggle="tooltip"]') : false;
		$o.navwrp = $('.nav-wrp').length > 0 && $o.r ? $('.nav-wrp') : false;
		$o.navlink = $('.nav-wrp').find(".nav-links").length > 0 && $o.r ? $o.navwrp.find(".nav-links") : false;
		$o.fullwh = $("[data-fullwh='y']").length > 0 && $o.r ? $("[data-fullwh='y']") : false;
		$o.fullh = $("[data-fullh='y']").length > 0 && $o.r ? $("[data-fullh='y']") : false;
		$o.bg = $("[data-bg]").length > 0 && $o.r ? $("[data-bg]") : false;
		$o.bgcolor = $("[data-bgcolor]").length > 0 && $o.r ? $("[data-bgcolor]") : false;
		$o.gradient = $("[data-gradient]").length > 0 && $o.r ? $("[data-gradient]") : false;
		$o.videopop = $(".video-popup").length > 0 && $o.r ? $(".video-popup") : false;
		$o.setpop = $(".set-popup").length > 0 && $o.r ? $(".set-popup") : false;
		$o.countbox = $(".count-box").length > 0 && $o.r ? $(".count-box") : false;
		$o.tabwidget = $(".tab-widget").length > 0 && $o.r ? $(".tab-widget") : false;
		$o.tabsauto = $(".tabs-auto").length > 0 && $o.r ? $(".tabs-auto") : false;
		$o.carouselwidget = $(".carousel-widget").length > 0 && $o.r ? $(".carousel-widget") : false;
		$o.accordionwidget = $(".accordion-widget").length > 0 && $o.r ? $(".accordion-widget") : false;
		$o.swiperwidget = $(".swiper-widget").length > 0 && $o.r ? $(".swiper-widget") : false;
		$o.swipergallery = $(".swiper-gallery").length > 0 && $o.r ? $(".swiper-gallery") : false;
		$o.videobg = $(".videobg").length > 0 && $o.r ? $(".videobg") : false;
		$o.videwidget = $(".vide-widget").length > 0 && $o.r ? $(".vide-widget") : false;
		$o.othersection1 = $(".other-section-1").length > 0 && $o.r ? $(".other-section-1") : false;
		$o.popgallerywidget = $(".popgallery-widget").length > 0 && $o.r ? $(".popgallery-widget") : false;
		$o.bgslider = $("[data-bgslider]").length > 0 && $o.r ? $("[data-bgslider]") : false;
		$o.countdownwidget = $(".countdown-widget").length > 0 && $o.r ? $(".countdown-widget") : false;
		$o.filterwidget = $(".filter-widget").length > 0 && $o.r ? $(".filter-widget") : false;
		$o.gmapwidget = $(".gmap-widget").length > 0 && $o.r ? $(".gmap-widget") : false;
		$o.socialsection = $(".social-section").length > 0 && $o.r ? $(".social-section") : false;
		$o.instagramwidget = $(".instagram-widget").length > 0 && $o.r ? $(".instagram-widget") : false;
		$o.twitterwidget = $(".twitter-widget").length > 0 && $o.r ? $(".twitter-widget") : false;
		$o.formwidget = $(".form-widget").length > 0 && $o.r ? $(".form-widget") : false;
		$o.elparallax = $(".el-parallax").length > 0 && $o.r ? $(".el-parallax") : false;
		$o.stellar = $("[data-stellar]").length > 0 && $o.r ? $("[data-stellar]") : false;
		$o.elanimate = $("[data-animate-in]").length > 0 && $o.r ? $("[data-animate-in]") : false;
		$o.bLazy = $(".b-lazy").length > 0 && $o.r ? $(".b-lazy") : false;

		if ($o.r) {

			$('html').before('<!-- ' + package_ver + ' -->');

			$o.tooltip.tooltip({
				container: 'body'
			});

			if ($o.bLazy) {
				rgen.blazyload();
			}
		

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

			/* Apply ID on each sections
			********************************************/
			if (rgen.elcheck(".main-container section")) {
				$(".main-container section").each(function (index, el) {
					$(this).attr('id', rgen.uid());
				});
			}

			/* Apply full screen section
			********************************************/
			if ($o.fullwh) {
				for (var i = 0; i < $o.fullwh.length; i++) {
					rgen.fullwh($o.fullwh[i]);
					var fullwhSection = $o.fullwh[i];
					$(window).resize(function () {
						rgen.fullwh(fullwhSection);
					});
				}
			}
			if ($o.fullh) {
				for (var i = 0; i < $o.fullh.length; i++) {
					if ($($o.fullh[i]).attr('data-fullh-wrp')) {
						rgen.fullh($o.fullh[i], $($o.fullh[i]).attr('data-fullh-wrp'));

						$(window).resize(function () {
							rgen.fullh($o.fullh[i], $($o.fullh[i]).attr('data-fullh-wrp'));
						});
					} else {
						rgen.fullh($o.fullh[i]);

						$(window).resize(function () {
							rgen.fullh($o.fullh[i]);
						});
					}

				}
			}

			/* Apply background image
			********************************************/
			if ($o.bg) {
				for (var i = 0; i < $o.bg.length; i++) {
					$($o.bg[i]).css({ backgroundImage: "url(" + $($o.bg[i]).attr("data-bg") + ")" });
				}
			}
			if ($o.bgcolor) {
				for (var i = 0; i < $o.bgcolor.length; i++) {
					$($o.bgcolor[i]).css({ backgroundColor: $($o.bgcolor[i]).attr("data-bgcolor") });
				}
			}

			if ($o.gradient) {
				for (var i = 0; i < $o.gradient.length; i++) {
					$o.gradient[i]

					var grd_colors = $($o.gradient[i]).attr('data-g-colors'),
						grd_color = grd_colors.split('|');

					$($o.gradient[i]).css({
						//background: grd_color[0],
						//background: "-moz-linear-gradient(top, " + grd_color[0] + " 0%, " + grd_color[1] + " 100%)",
						//background: "-webkit-linear-gradient(top, " + grd_color[0] + " 0%, " + grd_color[1] + " 100%)",
						background: "linear-gradient(to bottom, " + grd_color[0] + " 0%, " + grd_color[1] + " 100%)",
						//filter: "progid:DXImageTransform.Microsoft.gradient( startColorstr='" + grd_color[0] + "', endColorstr='" + grd_color[1] + "',GradientType=0 )"
					});
				}
			}


			/* Parallax background image
			********************************************/
			if ($o.elparallax) {
				for (var i = 0; i < $o.elparallax.length; i++) {
					rgen.parallax($o.elparallax[i], 'element');
				}
			}
			if ($o.stellar) {

				for (var i = 0; i < $o.stellar.length; i++) {
					$($o.stellar[i]).parent().css({ overflow: 'hidden' });
				}
				

				$.stellar({
					positionProperty: 'transform',
					horizontalScrolling: false,
					hideDistantElements: false
				});
			}
			


			/* Animated element
			********************************************/
			if ($o.elanimate) {
				for (var i = 0; i < $o.elanimate.length; i++) {

					var animateobj = $($o.elanimate[i]),
						animatein = animateobj.attr('data-animate-in'),
						animatearr = animatein.indexOf('|') > -1 ? animatein.split('|') : animatein,
						animateclass = typeof animatearr == 'object' ? animatearr[0] : animatearr,
						animatedelay = typeof animatearr == 'object' ? animatearr[1] : 0;

					animateobj.css({
						'-webkit-animation-delay': animatedelay + 's',
						'animation-delay': animatedelay + 's'
					});

					animateobj.viewportChecker({
						classToAdd: 'animated ' + animateclass,
						offset: 100
					});
				}
			}



			/* Video popup
			********************************************/
			if ($o.videopop) {
				for (var i = 0; i < $o.videopop.length; i++) {
					rgen.videoPopup($o.videopop[i]);
				}
			}

			/* Normal popup
			********************************************/
			if ($o.setpop) {
				for (var i = 0; i < $o.setpop.length; i++) {
					$o.setpop[i]

					var pop = $($o.setpop[i]).attr('href');
					$($o.setpop[i]).magnificPopup({
						type: 'inline',
						preloader: false,
						callbacks: {
							beforeOpen: function () {
								$(pop).removeClass('animate fadeInDown').addClass('animate fadeInDown');
							}
						}
					});
				}
			}

			/* Count box
			********************************************/
			if ($o.countbox) {
				var counterup_script_arr = [
					"//cdnjs.cloudflare.com/ajax/libs/waypoints/2.0.3/waypoints.min.js",
					"lib/counter-up/jquery.counterup.min.js"
				];

				rgen.getMultiScripts(counterup_script_arr, '').done(function () {
					$o.countbox.find('.count').counterUp();
				});
				
				//$('.count-box .count').counterUp();
			};

			/* Tab widget
			********************************************/
			if ($o.tabwidget) {
				for (var i = 0; i < $o.tabwidget.length; i++) {
					rgen.tabs($($o.tabwidget[i]).find('[data-tb]'));
				}
			}

			if ($o.tabsauto) {
				for (var i = 0; i < $o.tabsauto.length; i++) {
					var tabObj = {
						count: i,
						tb: $o.tabsauto[i]
					}
					rgen.tabs(tabObj);
				}
			}


			/* Carousel widget
			********************************************/
			if ($o.carouselwidget) {
				for (var i = 0; i < $o.carouselwidget.length; i++) {
					// SET ID ON ALL OBJECTS
					var owlObj = 'owl' + i;
					$($o.carouselwidget[i]).css({ opacity: 0 }).attr("id", owlObj).addClass(owlObj);
					rgen.slider("#" + owlObj);
				}
			}

			/* Accordion widget
			********************************************/
			if ($o.accordionwidget) {
				for (var i = 0; i < $o.accordionwidget.length; i++) {
					// SET ID ON ALL OBJECTS
					rgen.setId($o.accordionwidget[i], 'accwidget', i);
					rgen.accordion($o.accordionwidget[i]);
				}
			}

			/* Swiper widget
			********************************************/
			if ($o.swiperwidget) {
				for (var i = 0; i < $o.swiperwidget.length; i++) {
					// SET ID ON ALL OBJECTS
					var swiObj = 'swiper' + i;
					$($o.swiperwidget[i]).css({ opacity: 0 }).attr("id", swiObj).addClass(swiObj);
					rgen.swiper_slider("#" + swiObj);
				}
			}
			// Swiper gallery mode
			if ($o.swipergallery) {
				for (var i = 0; i < $o.swipergallery.length; i++) {
					// SET ID ON ALL OBJECTS
					var swiGal = 'swiperGallery' + i;
					$($o.swipergallery[i]).css({ opacity: 0 }).attr("id", swiGal).addClass(swiGal);
					rgen.swiper_gallery("#" + swiGal);
				}
			}


			/* video background
			********************************************/
			if ($o.videobg) {
				var mbyt_script_arr = ["lib/jquery.mb.YTPlayer/jquery.mb.YTPlayer.min.js"];
				rgen.getMultiScripts(mbyt_script_arr, '').done(function () {
					for (var i = 0; i < $o.videobg.length; i++) {
						rgen.videoBg($o.videobg[i]);
					}
				});
				
			};
			if ($o.videwidget) {
				var vide_script_arr = ["lib/Vide/jquery.vide.min.js"];
				rgen.getMultiScripts(vide_script_arr, '').done(function () {
					for (var i = 0; i < $o.videwidget.length; i++) {
						rgen.setId($o.videwidget[i], 'videwidget', i);
						rgen.vide($o.videwidget[i]);
					}
				});
			}

			/* Simple pop up gallery
			********************************************/
			if ($o.popgallerywidget) {
				for (var i = 0; i < $o.popgallerywidget.length; i++) {
					$o.popgallerywidget[i]

					$($o.popgallerywidget[i]).attr("id", 'popgallery' + i).addClass('popgallery' + i);

					$('#popgallery' + i).magnificPopup({
						delegate: '.pop-img',
						type: 'image',
						tLoading: 'Loading image #%curr%...',
						mainClass: 'mfp-img-mobile',
						gallery: {
							enabled: true,
							navigateByImgClick: true,
							preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
						},
						image: {
							tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
							titleSrc: function (item) {
								return item.el.attr('title');
							}
						}
					});
				}
			}

			/* Background slider
			********************************************/
			if (rgen.elcheck($o.bgslider)) {
				var vages_script_arr = [
					"lib/vegas/vegas.min.js"
				];

				rgen.getMultiScripts(vages_script_arr, '').done(function () {
					for (var i = 0; i < $o.bgslider.length; i++) {

						var s1 = $($o.bgslider[i]).attr('data-bgslider'),
							s2 = s1.split('|'),
							bgslides = [];

						$.each(s2, function (index, val) {
							bgslides.push({ src: val });
						});

						$($o.bgslider[i]).vegas({
							delay: 6000,
							slides: bgslides,
							timer: false,
							animation: 'kenburns'
						});
					}
				});
			};

			/* Countdown
			********************************************/
			if ($o.countdownwidget) {
				for (var i = 0; i < $o.countdownwidget.length; i++) {
					$($o.countdownwidget[i]).children('div').attr("id", 'countdown' + i);
					rgen.countdown("#countdown" + i);
				}
			}

			/* Filter widget
			********************************************/
			if ($o.filterwidget) {
				for (var i = 0; i < $o.filterwidget.length; i++) {
					$o.filterwidget[i]
					rgen.setId($o.filterwidget[i], 'filterwidget', i);
					rgen.filter($o.filterwidget[i]);
				}
			}

			/* Google map widget
			********************************************/
			if ($o.gmapwidget) {
				var social_script_arr = [
					"https://maps.googleapis.com/maps/api/js?sensor=false",
					"lib/MapIt/jquery.mapit.min.js"
				];

				rgen.getMultiScripts(social_script_arr, '').done(function () {
					for (var i = 0; i < $o.gmapwidget.length; i++) {
						rgen.setId($o.gmapwidget[i], 'gmapwidget', i);
						rgen.gmapset($o.gmapwidget[i]);
					}
				});
			}


			/* Social feeds
			********************************************/
			if ($o.socialsection) {

				var social_script_arr = [
					"bower_components/codebird-js/codebird.js",
					"bower_components/doT/doT.min.js",
					"bower_components/moment/moment.min.js",
					"js/jquery.socialfeed.js"
				];

				rgen.getMultiScripts(social_script_arr, 'lib/social-feed/').done(function () {

					// TWITTER
					if ($o.twitterwidget) {
						for (var i = 0; i < $o.twitterwidget.length; i++) {
							rgen.setId($o.twitterwidget[i], 'twitterwidget', i);
							rgen.twitter($o.twitterwidget[i]);
						}
					}

				});
			}


			/* Form widget
			********************************************/
			if ($o.formwidget) {
				for (var i = 0; i < $o.formwidget.length; i++) {
					$o.formwidget[i]
					rgen.formWidget($o.formwidget[i]);
					if ($('html').hasClass('builder')) {
						$($o.formwidget[i]).find('button').attr('disabled', true);
					} else {
						$($o.formwidget[i]).find('button').attr('disabled', false);
					}
				}
			};

			/* Demo menu
			********************************************/
			if ($('html').attr('data-demomenu') == 'y') {
				$.ajax({
					url: "demo-menu/all-demos.html"
				}).done(function(data) {
					$('body').append(data);
				});
			}


		} else {
			$o.r ? rgen.demo() : $('html').html('');
		}
	});

})();
