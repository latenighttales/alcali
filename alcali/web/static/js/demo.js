$(function () {
    activateNotificationAndTasksScroll();

    setSkinListHeightAndScroll(true);
    setSettingListHeightAndScroll(true);
    $(window).resize(function () {
        setSkinListHeightAndScroll(false);
        setSettingListHeightAndScroll(false);
    });
});

//Skin tab content set height and show scroll
function setSkinListHeightAndScroll(isFirstTime) {
    var height = $(window).height() - ($('.navbar').innerHeight() + $('.right-sidebar .nav-tabs').outerHeight());
    var $el = $('.demo-choose-skin');

    if (!isFirstTime){
      $el.slimScroll({ destroy: true }).height('auto');
      $el.parent().find('.slimScrollBar, .slimScrollRail').remove();
    }

    $el.slimscroll({
        height: height + 'px',
        color: 'rgba(0,0,0,0.5)',
        size: '6px',
        alwaysVisible: false,
        borderRadius: '0',
        railBorderRadius: '0'
    });
}

//Setting tab content set height and show scroll
function setSettingListHeightAndScroll(isFirstTime) {
    var height = $(window).height() - ($('.navbar').innerHeight() + $('.right-sidebar .nav-tabs').outerHeight());
    var $el = $('.right-sidebar .demo-settings');

    if (!isFirstTime){
      $el.slimScroll({ destroy: true }).height('auto');
      $el.parent().find('.slimScrollBar, .slimScrollRail').remove();
    }

    $el.slimscroll({
        height: height + 'px',
        color: 'rgba(0,0,0,0.5)',
        size: '6px',
        alwaysVisible: false,
        borderRadius: '0',
        railBorderRadius: '0'
    });
}

//Activate notification and task dropdown on top right menu
function activateNotificationAndTasksScroll() {
    $('.navbar-right .dropdown-menu .body .menu').slimscroll({
        height: '254px',
        color: 'rgba(0,0,0,0.5)',
        size: '4px',
        alwaysVisible: false,
        borderRadius: '0',
        railBorderRadius: '0'
    });
}

