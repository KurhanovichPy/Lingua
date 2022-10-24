type="text/javascript">
$(document).ready(function () {

    $(".modal-link").on("click", function() {

        $('.modal-overlay[data-modal-id="'+$(this).data('modal-id')+'"]').addClass("modal-overlay_visible");
        var dir_id = $(this).attr('data-id');
        document.getElementById("callback-form2").action = "/"+ dir_id +"/create";
    });

    $(".modal__close").on("click", function() {
        $(".modal-overlay").removeClass("modal-overlay_visible");
    });

    $(document).on("click", function(e) {
        if(!$(e.target).closest(".modal").length && !$(e.target).closest(".modal-link").length) {
            $(".modal-overlay").removeClass("modal-overlay_visible");
        }
    });
});