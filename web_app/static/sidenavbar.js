$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('showing');
        $('#main').toggleClass('showing');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});

$(function(){
    $('.links li a').filter(function(){return this.href==location.href}).parent().addClass('active').siblings().removeClass('active')
    $('.links li a').click(function(){
        $(this).parent().addClass('active').siblings().removeClass('active')
    })
});