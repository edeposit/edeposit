(function($) {
        var isTestingTitle = "robot framework testing mode";
        $.fn.setTestingMode = function(){
                window.name += isTestingTitle;
        };
        $.fn.unsetTestingMode = function (){
                window.name = window.name.split(isTestingTitle).join("");
        };
        $.fn.isTestingMode = function (){
                return (window.name.search(isTestingTitle) != -1);
        };
        var successCheckState = function (data){
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
        var checkState = function () {
                $.ajax(window.location + "/state")
                .done(successCheckState)
                .fail(function(){
                        setTimeout(checkState,1000);
                });
        };
        $(document).ready(function() {
                if( window.location.href.match("/originalfile-contributing/")){
                        setTimeout(checkState, 1000);
                }
        })
})(jQuery);
