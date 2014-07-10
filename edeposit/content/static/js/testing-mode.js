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
})(jQuery);
