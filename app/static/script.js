// $(function() {

//   $('.get-bitcoin-button').on('click', function(){
//     $('.get-bitcoin').css("height", "100%")
//     // $('.get-bitcoin').toggleClass('go');
//     $('.get-cash').toggleClass('go');
//     $('.get-cash').hide();

//   });

//     $('.dash-link .get-bitcoin').one('click', function(){
        
//                                 $('.get-bitcoin-button').css({
//                                 "background-color" : "#FBB900",
//                                 "border" : "9px solid #2F2D27"
//                                 })
//                                 .append("<h1 style='color: #2F2D27'>Hi!</h1>")
//                                 // $.load("/insert/insert.html");
//                             //     $(".get-bitcoin").delay(1000).queue(function( nxt ) {
//                             //     $(this).load('/static/getbitcoin.html');
//                             //     nxt();
//                             // });
//                                 $('.bitcoin-header').hide();

//     });
// });

$('#link').one('click', function(ev){

    ev.preventDefault();

    var $self = $(this);

            $('.get-bitcoin-button').css(
                {"background-color" : "#FBB900",
                "border" : "9px solid #2F2D27"}), 
                $('.bitcoin-header').hide();
                //$('.get-bitcoin-button').append("<h1 style='color: #2F2D27'>{{ message }}</h1>" ); übergangsnachricht 
                // , function(){

                $(".get-bitcoin").delay(1000).queue(function( nxt ) {
                    document.location = $('#link').delay(10000).attr('href');
                    nxt();
                });

            // };


});






