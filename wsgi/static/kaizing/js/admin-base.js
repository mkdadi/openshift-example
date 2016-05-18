$(function(){
    $("[data-toggle='offcanvas']").click(function(e) {
        e.preventDefault();
        //If window is small enough, enable sidebar push menu
        if ($(window).width() <= 992) {
            var elem = $('.row-offcanvas');
            elem.toggleClass('active');
            $(".right-side").removeClass("strech");
            $('.left-side').removeClass("collapse-left");
            elem.toggleClass("relative");
        } else {
            //Else, enable content streching
            var chartChangeWidth = 220 / 2;
            if($('.right-side').hasClass('strech')){
                $(".right-side").removeClass("strech");
                chartChangeWidth = -chartChangeWidth;
            }else{
                $(".right-side").addClass("strech");
            }
            $('.left-side').toggleClass("collapse-left");
            $('.js-highchart-c2').each(function(){
                var chart = $(this).highcharts();
                chart.setSize(chart.chartWidth + chartChangeWidth, chart.chartHeight);
            });
        }
    });

    //Add hover support for touch devices
    $('.btn').bind('touchstart', function() {
        $(this).addClass('hover');
    }).bind('touchend', function() {
            $(this).removeClass('hover');
    });

    function activate_menue(current_path){
        var path_found = false;
        $('.js-nav').each(function(){
            if(!path_found && $(this).attr('href') == current_path){
                path_found = true;
                $(this).parent().addClass('active');
                if($(this).hasClass('nav-child')){
                    $(this).parents('.treeview').addClass('active');
                }
            }
        });
        return path_found;
    }
    var current_path = window.location.pathname;
    var path_found = false;
    while(!path_found){
        path_found = activate_menue(current_path);
        current_path = current_path.slice(0, -1);
        current_path = current_path.substring(0, current_path.lastIndexOf("/")+1);
        if(current_path == "/portal"){
            break;
        }
    }
    /* Sidebar tree view */
    $(".sidebar .treeview").tree();

    $('.hover-info-icon').click(function(){
        return false;
    });

});

/*
 * SIDEBAR MENU
 * ------------
 * This is a custom plugin for the sidebar menu. It provides a tree view.
 *
 * Usage:
 * $(".sidebar).tree();
 *
 * Note: This plugin does not accept any options. Instead, it only requires a class
 *       added to the element that contains a sub-menu.
 *
 * When used with the sidebar, for example, it would look something like this:
 * <ul class='sidebar-menu'>
 *      <li class="treeview active">
 *          <a href="#>Menu</a>
 *          <ul class='treeview-menu'>
 *              <li class='active'><a href=#>Level 1</a></li>
 *          </ul>
 *      </li>
 * </ul>
 *
 * Add .active class to <li> elements if you want the menu to be open automatically
 * on page load. See above for an example.
 */
(function($) {
    "use strict";

    $.fn.tree = function() {

        return this.each(function() {
            var btn = $(this).children("a").first();
            var menu = $(this).children(".treeview-menu").first();
            var isActive = $(this).hasClass('active');

            //initialize already active menus
            if (isActive) {
                menu.show();
                btn.children(".fa-angle-left").first().removeClass("fa-angle-left").addClass("fa-angle-down");
            }
            //Slide open or close the menu on link click
            btn.click(function(e) {
                e.preventDefault();
                if (isActive) {
                    //Slide up to close menu
                    menu.slideUp();
                    isActive = false;
                    btn.children(".fa-angle-down").first().removeClass("fa-angle-down").addClass("fa-angle-left");
                    btn.parent("li").removeClass("active");
                } else {
                    //Slide down to open menu
                    menu.slideDown();
                    isActive = true;
                    btn.children(".fa-angle-left").first().removeClass("fa-angle-left").addClass("fa-angle-down");
                    btn.parent("li").addClass("active");
                }
            });

            /* Add margins to submenu elements to give it a tree look */
            menu.find("li > a").each(function() {
                var pad = parseInt($(this).css("margin-left")) + 10;

                $(this).css({"margin-left": pad + "px"});
            });

        });

    };


}(jQuery));

function format_number(x){
    x = parseInt(x);
    var isnegative = x < 0;
    if(isnegative){
        x = -x;
    }
    x= x.toString();
    var lastThree = x.substring(x.length-3);
    var otherNumbers = x.substring(0,x.length-3);
    if(otherNumbers != '')
        lastThree = ',' + lastThree;
    var res = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree;
    if(isnegative){
        res = '-' + res;
    }
    return res;
}
