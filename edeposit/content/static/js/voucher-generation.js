(function($) {
        var hasVoucher = function (url){
                var state = data['state'];
                var canContribute = (state == 'contributingOfAnOriginalFile');
                if ( canContribute ){
                        if( $().isTestingMode() ) {
                                setTimeout(checkState,1000);
                        } else {
                                var originalFile = $.grep(data['relatedItems'],function(item){
                                        return item['to_object'].match("<OriginalFile at");
                                });
                                var newUrl = window.location.protocol + "//" + window.location.host
                                        + "/" + originalFile[0]['to_path'] + "/edit";
                                window.location = newUrl;
                        }
                } else {
                        setTimeout(checkState,1000);
                }
        };
        var checkVoucherGenerationState = function (base_href, numOfRetries) {
                if( numOfRetries <= 0 ) return;
                var handler = function(){
                        $.ajax(base_href + "/has-voucher").done(function(data){
                                if( data.has_voucher ){
                                        $('#formfield-form-widgets-voucher').html(
                                                data['voucher_widget_html']
                                        );
                                        $('.voucher-download')[0].click();
                                } else {
                                        checkVoucherGenerationState(base_href, numOfRetries - 1);
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
                        checkVoucherGenerationState(document.location.href,20);
                });
                return false;
        };

        $(function(){
                $(".generate-voucher").click(submitGeneration);
        });
})(jQuery);
