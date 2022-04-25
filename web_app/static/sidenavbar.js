$(document).ready(function () {
    // $("#sidebar").mCustomScrollbar({
    //     theme: "minimal"
    // });

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('showing');
        $('#main').toggleClass('showing');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });

    $('#newTeam').on('click', function () {
        location.href = "teams/new"
    });

    $('#newProject').on('click', function () {
        location.href = "projects/new"
    });

    $('#filterTeamMembers').on('keyup', function(){
        let value = document.getElementsByClassName('filter-list-input')[0].value.toUpperCase();
        // let list = document.getElementByClassName('form-group-users')[0].value;
        // let users = list.getElementsByClassName('teamMember')

        // for (i=0; i<users.length; i++) {
        //     let name = users[i].getElementsByClassName('memberName')[0].value
        //
        //     users[i].style.display = name.toUpperCase().indexOf(value) > -1 ? "" : "none";
        // }
        console.log(value);
        // console.log(list);
    });

    // $('#searchTeamMember').on('keyup', function(){
    //     // Access text value and elements from the DOM
    //     let value = $(#searchTeamMember).val().toUpperCase();
    //         // document.getElementById("searchTeamMember").value.toUpperCase();
    //     let list = $(#memberList)
    //         // document.getElementById("memberList");
    //     let users = list.getElementsByTagName("div");
    //
    // for (i = 0; i < users.length; i++) {
    //     let user = users[i].getElementsByClassName("memberName");
    //     // let first_name = user[0].textContent.split(" ")[0];
    //     // let last_name = user[1].textContent.split(" ")[1];
    //     let name = user[0].textContent;
    //
    //     users[i].style.display = name.toUpperCase().indexOf(value) > -1 ? "" : "none";
    // }
    // })
});

$(function(){
    $('.links li a').filter(function(){return this.href==location.href}).parent().addClass('active').siblings().removeClass('active')
    $('.links li a').click(function(){
        $(this).parent().addClass('active').siblings().removeClass('active')
    })
});
