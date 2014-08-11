(function ($) {
  Drupal.behaviors.myModule = function(context) {
    var externalScript = $('<script></script>').attr('type','text/javascript').attr('src', 'https://www.mypaga.com/paga-web/epay/ePay-button.paga?k=f7c2c32f-7c65-450c-b6c0-6c5ef43b6645&e=false');
    $('body').append(externalScript);
  }
}(jQuery));