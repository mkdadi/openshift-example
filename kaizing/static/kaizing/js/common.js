function isNumber(e){e=e?e:window.event;var t=e.which?e.which:e.keyCode;return t>31&&(48>t||t>57)?!1:!0}function activateCustomScroll(){mCustomScrollbar?$(".custom-scroll").mCustomScrollbar({scrollInertia:300,theme:"minimal-dark"}):setTimeout(function(){activateCustomScroll()},100)}function downloadCSSAtOnload(){var e=document.createElement("link");e.href="/static/css/style.min.css?v=4",e.rel="stylesheet",e.type="text/css",document.head.appendChild(e)}function slowscroll(){$("a[href*=#]:not([href=#])").click(function(){if(location.pathname.replace(/^\//,"")==this.pathname.replace(/^\//,"")&&location.hostname==this.hostname){var e=$(this.hash);if(e=e.length?e:$("[name="+this.hash.slice(1)+"]"),e.length)return $("html,body").animate({scrollTop:parseInt(e.offset().top)-parseInt($(".custom-menu").height())},1e3),!1}})}function setMenutype(){var e=new Date,t=e.getHours(),n="";return 15>t||t>22||22==t?n="lunch":t>15&&18>t||15==t?n="snacks":(t>18&&22>t||18==t)&&(n="dinner"),n}function getLocations(){$.ajax({method:"GET",url:"/api/v1/location/",dataType:"json",cache:"true"}).success(function(e){if("error"==e.status){var t=[],n=setMenutype();$("#hiddenMenuType").val(n),$.ajax({method:"GET",url:"/static/js/app/locations.json",dataType:"json"}).success(function(e){var t=e,n=$("#locationSelect");$.each(t,function(){n.append($("<option />").val(this.location_id).text(this.drop_point))}),$.cookie("location_id")?$("#locationSelect").dropdown("set value",$.cookie("location_id")).dropdown("destroy").dropdown():$("select").dropdown();var a=$("#subscribe-select");$.each(t,function(){a.append($("<option />").val(this.drop_point).text(this.drop_point))}),$("#subscribe-select").dropdown()})}else if("success"==e.status){var t=e.data,a=$("#locationSelect");$.each(t,function(){a.append($("<option />").val(this.location_id).text(this.location_name))}),$.cookie("location_id")?$("#locationSelect").dropdown("set value",$.cookie("location_id")).dropdown("destroy").dropdown():$("select").dropdown();var o=$("#subscribe-select");$.each(t,function(){o.append($("<option />").val(this.location_name).text(this.location_name))}),$("#subscribe-select").dropdown();var n=setMenutype();$("#hiddenMenuType").val(n)}}).error(function(){$.ajax({method:"GET",url:"/static/js/app/locations.json",dataType:"json"}).success(function(e){var t=[];t=e;var n=$("#locationSelect");$.each(t,function(){n.append($("<option />").val(this.location_id).text(this.drop_point))}),$.cookie("location_id")?$("#locationSelect").dropdown("set value",$.cookie("location_id")).dropdown("destroy").dropdown():$("select").dropdown();var a=$("#subscribe-select");$.each(t,function(){a.append($("<option />").val(this.drop_point).text(this.drop_point))}),$("#subscribe-select").dropdown();var o=setMenutype();$("#hiddenMenuType").val(o)})})}function expandSelect(){{var e=document.getElementById("select_flag").value;$(".locationselect.selection")}1==e?($(".dropdown.locationselect").dropdown("hide"),document.getElementById("select_flag").value=0):($(".dropdown.locationselect").dropdown("show"),document.getElementById("select_flag").value=1)}function menuPage(){if($("#locationSelect").val()){var e=new Date,t=new Date(e.getFullYear(),e.getMonth()+3,e.getDate());$.cookie("location_id",$("#locationSelect").val(),{expires:t}),$.cookie("mealtype",$("#hiddenMenuType").val()),window.location.replace("/app/")}else expandSelect()}function submit_subscription(){if($('input[name="phone"]').val().length<10)return alert("Phone number can not be less than 10 digits"),!1;if("0"==$('input[name="phone"]').val()[0])return alert("First digit can't be zero."),!1;if(""==$('input[name="name"]').val())return $('input[name="name"]').focus(),!1;if(""==$('input[name="email"]').val())return $('input[name="email"]').focus(),!1;if($('input[name="email"]')&&!validateEmail($('input[name="email"]').val()))return $('input[name="email"]').focus(),alert("Invalid email!"),!1;if(""==$('input[name="location"]').val())return $('input[name="location"]').focus(),!1;var e={name:$("input[name='name']").val(),phone:$("input[name='phone']").val(),email:$("input[name='email']").val(),location:$("input[name='location']").val()};$("#subscribe_div .form").addClass("loading"),$.ajax({type:"POST",url:"/box/wantsub/",data:JSON.stringify(e),success:function(){$("#subscribe_div .form").removeClass("loading"),$("#subscribe_div").hide(),$("#thanks-div").show(),$(":input","#subscribe_div").not(":button, :submit, :reset, :hidden").val("").removeAttr("checked").removeAttr("selected")},error:function(){$("#subscribe_div .form").removeClass("loading"),window.location.reload()}})}function showsubs(){$("#subscribe_div").show(),$("#thanks-div").hide(),$(":input","#subscribe_div .form").not(":button, :submit, :reset, :hidden").val("").removeAttr("checked").removeAttr("selected")}function hideModal(e){"click"===e.type&&$("#subscription_modal").slideToggle(500,"linear",function(){$("body").removeClass("stop-scrolling"),$("#subscription_modal").toggleClass("display-block")})}function validateEmail(e){var t=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;return t.test(e)}function send_feedback(){if($('input[name="feedback_phone"]').val()&&$('input[name="feedback_phone"]').val().length<10)return alert("Phone number can not be less than 10 digits"),!1;if("0"==$('input[name="feedback_phone"]').val()[0])return alert("First digit can't be zero."),!1;if(""==$('input[name="feedback_phone"]').val())return $('input[name="feedback_phone"]').focus(),!1;if(""==$('input[name="feedback_name"]').val())return $('input[name="feedback_name"]').focus(),!1;if($('input[name="feedback_email"]').val()&&!validateEmail($('input[name="feedback_email"]').val()))return $('input[name="feedback_email"]').focus(),!1;if(""==$('textarea[name="feedback_msg"]').val())return $('textarea[name="feedback_msg"]').focus(),!1;var e={name:$("input[name='feedback_name']").val(),phone:$("input[name='feedback_phone']").val(),email:$("input[name='feedback_email']").val(),feedback:$('textarea[name="feedback_msg"]').val()};$.ajax({type:"POST",url:"/api/v1/genfeed/",data:JSON.stringify(e),success:function(){$("#feedbackdiv").hide(),$("#feedbackthanksdiv").show()},error:function(){window.location.reload()}})}$(document).ready(function(){var e=$(window).height();minheight=(e-70).toString(),$(".main-container").css({"min-height":minheight+"px"})}),$(".hamburger-icon").click(function(e){$(this).toggleClass("active"),$(this).hasClass("active")?$(".desktop-nav").slideToggle(300,"linear",function(){$(".desktop-nav").show()}):$(".desktop-nav").slideToggle(300,"linear",function(){$(".desktop-nav").hide()}),$("#subscription_modal").hasClass("display-block")&&($("#subscription_modal").removeClass("display-block"),$("#subscription_modal").hide(500,"linear")),e.preventDefault()}),$("#modalSubmit").click(function(){var e=$("#email").val(),t=$("#phone").val();if(e||t){if(e||t){e||(e="null"),t||(t="null");var n={set:"lead_cupcake",phone:t,email:e};$(".submitButton").addClass("loading"),$.ajax({method:"POST",url:"/web.php",headers:{"Content-Type":"application/x-www-form-urlencoded"},data:$.param(n)}).success(function(){$(".submitButton").removeClass("loading"),$("#friendshipdayform").hide(),$("#submitformmsg").html('<p class="submitMsg">Thanks for showing your interest. We will get back to you soon.<i class="smile icon"></i></p>'),setTimeout(function(){$(".ui.modal").modal("hide")},2300)}).error(function(){$(".submitButton").removeClass("loading"),$("#friendshipdayform").hide(),$("#submitformmsg").html('<p class="submitMsg">Thanks for showing your interest. We will get back to you soon.<i class="smile icon"></i></p>'),setTimeout(function(){$(".ui.modal").modal("hide")},2300)})}}else $("#email").focus()}),$(".cupcakesbar").click(function(){$("#submitformmsg").empty(),$("#friendshipdayform input").val(""),$("#friendshipdayform").show()});