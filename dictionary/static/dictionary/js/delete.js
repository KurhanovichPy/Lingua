type="text/javascript">
$(document).ready(function () {

    $(".modal-link").on("click", function() {

        $('.modal-overlay[data-modal-id="'+$(this).data('modal-id')+'"]').addClass("modal-overlay_visible");
        var element_id = $(this).attr('data-id');
        var word = $(this).attr('data-word');
        document.getElementById("callback-form1").action = "/word/"+ element_id +"/delete";
        document.getElementById("delete-word").innerHTML = "Are you sure you want to delete &quot;" + word +"&quot; ?";
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