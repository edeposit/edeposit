(function($) {
        var isTesting = false;
        
        var successCheckState = function (data){
                var state = data['state'];
                var canContribute = (state == 'contributingOfAnOriginalFile');
                if ( canContribute ){
                        if( !isTesting ) {
                                var originalFile = $.grep(data['relatedItems'],function(item){
                                        return item['to_object'].match("<OriginalFile at");
                                });
                                var newUrl = window.location.protocol + "//" + window.location.host
                                + "/" + originalFile[0]['to_path'] + "/edit";
                                window.location = newUrl;
                        };
                } else {
                        setTimeout(checkState);
                }
        };
        var checkState = function () {
                $.ajax(window.location + "/state")
                .done(successCheckState)
                .fail(function(){
                        setTimeout(checkState);
                });
        };
        $.fn.setEDepositRequestIsTesting = function (isTesting){
                isTesting = isTesting;
        };
        $(document).ready(function() {
                if( window.location.href.match("/originalfile-contributing/")){
                        setTimeout(checkState, 1000);
                }
        })
})(jQuery);
