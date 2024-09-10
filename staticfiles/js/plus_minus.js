$(document).ready(function () {
  $(".section-title.toggleable").click(function () {
    // Close all other sections
    $(".section-title.toggleable").not(this).removeClass("active text-success");
    $(".section-content").not($(this).next()).slideUp(300);
    
    // Toggle the clicked section
    $(this).toggleClass("active text-success");
    $(this).next(".section-content").slideToggle({
      duration: 300,
      complete: function () {
        $(this).css('overflow', 'visible');
      }
    });
  });
});