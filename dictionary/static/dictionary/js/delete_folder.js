type="text/javascript">
$(document).ready(function () {

    $(".modal-link").on("click", function() {

        $('.modal-overlay[data-modal-id="'+$(this).data('modal-id')+'"]').addClass("modal-overlay_visible");
        var element_id = $(this).attr('data-pk');
        var name = $(this).attr('data-name');
        document.getElementById("callback-form3").action = "/"+ element_id +"/delete";
        document.getElementById("delete-folder").innerHTML = "Are you sure you want to delete &quot;" + name +"&quot; ?";
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