angular.module('limberApp').controller('LandingController', function($scope){
    $(".animation").typed({
        strings: ["agile software development", "taking your girlfriend to shop", "better project management."],
        typeSpeed: 70,
        backDelay: 70,
        cursorChar: " | "
     });
});
