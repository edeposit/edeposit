(function($) {
        var checkGenerationState = function (base_href, numOfRetries) {
                if( numOfRetries <= 0 ) return;
                var handler = function(){
                        $.ajax(base_href + "/has-voucher").done(function(data){
                                if( data.has_voucher ){
                                        $('#formfield-form-widgets-voucher').html(
                                                data['voucher_widget_html']
                                        );
                                        $('.voucher-download')[0].click();
                                } else {
                                        checkGenerationState(base_href, numOfRetries - 1);
                                };
                                
                        });
                };
                setTimeout(handler,1000);
        };
        var submitGeneration = function(event){
                event.preventDefault();
                var href = $(this).attr('href');
                var element = $(this);
                $.ajax(href).done(function(data){
                        $(element).hide();
                        $('.voucher-is-generating').fadeIn();
                        $('.not-voucher-spinner').fadeIn();
                        checkGenerationState(document.location.href,20);
                });
                return false;
        };

        $(function(){
                $(".generate-voucher").click(submitGeneration);
        });
})(jQuery);
