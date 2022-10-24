type="text/javascript">
$(document).ready(function () {

    $(".modal-link").on("click", function() {

        $('.modal-overlay[data-modal-id="'+$(this).data('modal-id')+'"]').addClass("modal-overlay_visible");
        var element_id = $(this).attr('data-update-id');
        var native_word = $(this).attr('data-update-native');
        var translate_word = $(this).attr('data-update-translate');
        document.getElementById("callback-form5").action = "/"+ element_id +"/update";
        document.getElementById("native_word").value = native_word;
        document.getElementById("translate_word").value = translate_word;
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