$(function(){
    $(".mark").mouseover(function () {
        $(".float-box").css("display","block");
        $(".big-box").css("display","block");
    });

    $(".mark").mouseout(function () {
        $(".float-box").css("display","none");
        $(".big-box").css("display","none");
    });

    $(".mark").mousemove(function (e) {
        var _event = e || window.event;  //兼容多个浏览器的event参数模式

        var float_box_width  = $(".float-box")[0].offsetWidth;
        var float_box_height = $(".float-box")[0].offsetHeight;//175,175

        var float_box_width_half  =  float_box_width / 2;
        var float_box_height_half =  float_box_height/ 2;//87.5,87.5

        var small_box_width  =  $(".outer")[0].offsetWidth;
        var small_box_height =  $(".outer")[0].offsetHeight;//360,360

        var mouse_left = _event.clientX   - float_box_width_half;
        var mouse_top = _event.clientY  - float_box_height_half;

        if (mouse_left < 0) {
            mouse_left = 0;
        } else if (mouse_left > small_box_width - float_box_width) {
            mouse_left = small_box_width - float_box_width;
        }
        if (mouse_top < 0) {
            mouse_top = 0;
        } else if (mouse_top > small_box_height - float_box_height) {
            mouse_top = small_box_height - float_box_height;
        }

        $(".float-box").css("left",mouse_left + "px");
        $(".float-box").css("top",mouse_top + "px");

        if(mouse_left>=500){
            $(".big-box").css("left",(mouse_left-350) + "px");
            $(".big-box").css("top",mouse_top + "px");
        }
        else
        {
            $(".big-box").css("left",(mouse_left+175) + "px");
            $(".big-box").css("top",mouse_top + "px");
        }


        var percentX = ($(".big-box img")[0].offsetWidth - $(".big-box")[0].offsetWidth) / (small_box_width - float_box_width);
        var percentY = ($(".big-box img")[0].offsetHeight - $(".big-box")[0].offsetHeight) / (small_box_height - float_box_height);

        $(".big-box img").css("left",-percentX * mouse_left + "px");
        $(".big-box img").css("top",-percentY * mouse_top + "px")
    })
})
