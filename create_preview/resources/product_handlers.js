$(document).ready(function() {
    let preview_pic = $(".product-single__media-group")
    let show_preview = $("#show_preview")
    let data = $("#custom_options_form :input")

    let paper_size = $("#SingleOptionSelector-0")
    let paper_stock = $("#SingleOptionSelector-1")
    let quantity = $("#SingleOptionSelector-2")

    show_preview.click(function(e) {
        e.preventDefault()
        let data_content = data.serializeArray()
        
        let data_payload = {
            "font_type": data_content.filter((e) => {return e.name == "fonts"})[0].value,
            "paper_type": convert_paper_size(paper_size.val()),
            "paper_color": convert_paper_stock(paper_stock.val()),
            "alignment": "right_left",
            "text_color": data_content.filter((e) => {return e.name == "text-color"})[0].value,
            "quantity": quantity.val(),
            "lines": {
                "line1": data_content.filter((e) => {return e.name == "line1"})[0].value,
                "line2": data_content.filter((e) => {return e.name == "line2"})[0].value,
                "line3": data_content.filter((e) => {return e.name == "line3"})[0].value,
                "line4": data_content.filter((e) => {return e.name == "line4"})[0].value
            }
        }

        update_photo(data_payload)
    })

    let update_photo = function(data_payload){
        let element_html = `<div id="FeaturedMedia-pp-preview-pic-wrapper" data-product-single-media-wrapper="" data-media-id="" tabindex="-1" class="product-single__media-wrapper js"> <style>#FeaturedMedia-pp-preview-pic{max-width: 386.0px; max-height: 493px;}#FeaturedMedia-pp-preview-pic-wrapper{max-width: 386.0px;}</style> <img id="FeaturedMedia-pp-preview-pic" class="feature-row__image product-featured-media lazyautosizes ls-is-cached lazyloaded" src=""></div>`
        // Get the photo from server
        $.ajax({
            type:"GET",
            url: "https://the-paper-place-australia.myshopify.com/apps/generate-image",
            data: {"json": JSON.stringify(data_payload)},
            success: function(returned_data){
                console.log(returned_data)
                if($("#FeaturedMedia-pp-preview-pic").length){
                    $("#FeaturedMedia-pp-preview-pic").attr('src', returned_data)
                } else {
                    preview_pic.append(element_html)
                    $("#FeaturedMedia-pp-preview-pic").attr('src', returned_data)
                }
            }
        }).done(function(){
            preview_pic.children().addClass("hide")
            $("#FeaturedMedia-pp-preview-pic-wrapper").removeClass("hide")
        }).fail(function() {
            alert("There was an error generating a preview. Please try again.")
        }).always(function(){
            alert("All done.")
        })
        
        //Check to see if image already exists
            // If yes, just change source attr
            
            // If no, add classes for lightbox
            // Add to preview pic list

        // Add 'hide' class to all other nodes in list
        // Check if photo has hide class, if yes then remove
    }

    let convert_paper_stock = function(paper_color_value){
        switch(paper_color_value){
            case "Oxford Cream": return "oxford_cream"
            case "Oxford White": return "oxford_white"
            case "Rives Sand": return "rives_sand"
            case "Rives Wheat": return "rives_wheat"
            case "Rives White": return "rives_white"
            case "Speckletone": return "speckletone"
            case "Superfine White": return "superfine_white"
        }
    }

    let convert_paper_size = function(paper_size_value){
        switch(paper_size_value){
            case "A5": return "a5_paper"
            case "A6": return "a6_paper"
        }
    }
})