var J = jQuery.noConflict();

J(document).ready(function(){

        // Drop Menu
        function mainmenu(){
        J(".nav ul ").css({display: "none"}); // Opera Fix
        J(".nav li").hover(function(){
                        J(this).find('ul:first').css({visibility: "visible",display: "none"}).slideDown(200);
                        },function(){
                        J(this).find('ul:first').css({visibility: "hidden"});
                        });
        }

        mainmenu();

        // Fade Icons
        J("img.a").hover(
                function() {
                J(this).stop().animate({"opacity": "0"}, "fast");
                },
                function() {
                J(this).stop().animate({"opacity": "1"}, "fast");
        });

        // Fade Hover Links
        J(".entry-title a").hover(
        function() {
                J(this).animate({"opacity": ".7"}, "fast");
                        },
                function() {
                        J(this).animate({"opacity": "1"}, "fast");
        });

        // Remove Margins
        J(".flickrPhotos > li:nth-child(2n)").addClass('remove-margin');
        J('#sidebar > div').last().addClass('last-sidebar');



        J(".lightbox").live('mouseover', function(){
            J(this).fancybox({
                'titlePosition' 	: 'over',
                'overlayColor'		: '#ddd',
                'overlayOpacity'	: 0.9,
                'transitionIn'	: 'slow',
                'transitionOut'	: 'slow',
                'speedIn' : '1400',
                'speedOut' : '1400',
                'easingIn' : 'easeOutBounce',
                'easingOut' : 'easeOutBounce'
            }).die('click');
            return false;
        });

        J(".iframe").fancybox({
                'titlePosition'		: 'outside',
                'overlayColor'		: '#ddd',
                'overlayOpacity'	: 0.9,
                'titleShow'			: 'false',
                'transitionIn'	: 'slow',
                'transitionOut'	: 'slow',
                'speedIn' : '1400',
                'speedOut' : '1400',
                'easingIn' : 'easeOutBounce',
                'easingOut' : 'easeOutBounce',
                'width' : 400,
                'height' : 340,
                'autoDimensions' : false,
                'type': 'iframe',
                'onClosed' : function() {
                    window.location = window.location.href;
                }
        });


        J(".apps").live('mouseover', function(){
            J(this).fancybox({
                'titlePosition'		: 'outside',
                'overlayColor'		: '#ddd',
                'overlayOpacity'	: 0.9,
                'titleShow'			: 'false',
                'transitionIn'	: 'slow',
                'transitionOut'	: 'slow',
                'speedIn' : '1400',
                'speedOut' : '1400',
                'easingIn' : 'easeOutBounce',
                'easingOut' : 'easeOutBounce',
                'width' : 800,
                'height' : 600,
                'autoDimensions' : false,
                'type': 'iframe',
            }).die('click');
            return false;
        });

        J(".iframe_convidar").fancybox({
                'titlePosition'		: 'outside',
                'overlayColor'		: '#ddd',
                'overlayOpacity'	: 0.9,
                'titleShow'			: 'false',
                'transitionIn'	: 'slow',
                'transitionOut'	: 'slow',
                'speedIn' : '1400',
                'speedOut' : '1400',
                'easingIn' : 'easeOutBounce',
                'easingOut' : 'easeOutBounce',
                'width' : 335,
                'height' : 500,
                'autoDimensions' : false,
                'type': 'iframe',
        });


});