$(document).ready(function() {
    let preview_pic = $(".product-single__photos")
    let show_preview = $("#show_preview")
    let data = $("#custom_options_form :input")

    let paper_size = $("#ProductSelect-p-stationery-template-option-0")
    let paper_stock = $("#ProductSelect-p-stationery-template-option-1")
    let quantity = $("#ProductSelect-p-stationery-template-option-2")

    let font_selector = $("#fonts")

    let update_font_selector = function() {
        const value = font_selector.val()
        const font = convert_font(value)

        font_selector.css('font-family', font)
    }

    show_preview.click(function(e) {
        e.preventDefault()
        let data_content = data.serializeArray()
        
        let data_payload = {
            "font_type": data_content.filter((e) => {return e.name == "fonts"})[0].value,
            "paper_type": convert_paper_size(paper_size.val()),
            "paper_color": convert_paper_stock(paper_stock.val()),
            "alignment": data_content.filter((e) => {return e.name =="alignment"})[0].value,
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

    let showRelevant = function () {
        let thumbs = $('#ProductThumbs').children()
        let size = $('#ProductSelect-p-stationery-template-option-0').val().toLowerCase()
       
        thumbs.each(function(index, thumbnail) {
            let thumbShow = $(this).children().attr('href').toLowerCase().indexOf(size) >= 0
            if (!thumbShow) {
                $(this).css("margin-bottom", "0px")
                $(this).find("a").attr("class", "hide")
                $(this).find("img").attr("class", "hide")
            } else {
                $(this).css("margin-bottom", "30px")
                $(this).find("a").removeAttr("class", "hide")
                $(this).find("img").removeAttr("class", "hide")
            }
        })
    }
    
    let updateSelectorStyles = function(){
        let selectors = $('.selector-wrapper')
        selectors.css({"display": "inline-block", "margin-right": "10px"})
    }

    let update_photo = function(data_payload){
        let element_html = 
        `<style>
        #ProductImage-Featured {
          max-width: 386px;
          max-height: 493px;
        }
        #ProductImageWrapper-Featured {
          max-width: 386px;
        }
        </style>
        
        <div id="ProductImageWrapper-Featured" class="product-single__image-wrapper supports-js zoom-lightbox" data-image-id="">
        <div style="padding-top:127.7202073%;">
          <img id="ProductImage-Featured" class="product-single__image lazyautosizes lazyloaded" src="">
        </div>
      </div>`
        // Get the photo from server
        $.ajax({
            type:"GET",
            url: "https://the-paper-place-australia.myshopify.com/apps/generate-image/generate-image?json="+encodeURIComponent(JSON.stringify(data_payload)),
            success: function(returned_data){
                console.log(returned_data)
                if($("#ProductImageWrapper-Featured").length){
                    $("#ProductImage-Featured").attr('src', returned_data)
                } else {
                    preview_pic.append(element_html)
                    $("#ProductImage-Featured").attr('src', returned_data)
                }
            }
        }).done(function(){
            preview_pic.children().addClass("hide")
            $("#ProductImageWrapper-Featured").removeClass("hide")
        }).fail(function() {
            alert("There was an error generating a preview. Please try again.")
        }).always(function(){
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

    let convert_font = function(value) {
        switch(value.toLowerCase()){
            case 'bernhard': return 'b'
            case 'garamond': return 'gar'
            case 'gabriola': return 'gab'
            case 'shelley_allegro': return 'shell'
            default: return 'Aria'
        }
    }

    let updateClickable = function(){
        selector = $(".cod_clickable")
        selector.each(function(index, node) {
            if($(this).children("input").prop('checked')?true:false){
                $(this).css('border-color', "#add8e6")
                $(this).css('border-style', "solid")
                $(this).css('border-thickness', "3px")
            } else {
                $(this).css('border', "none")
            }
        })  
    }

    font_selector.on("load", update_font_selector)
    font_selector.on("change", update_font_selector)

    $("#ProductSelect-p-stationery-template-option-0").on("load", showRelevant)
    $("#ProductSelect-p-stationery-template-option-0").on("change", showRelevant)
    
    $(".cod_clickable").on('load', updateClickable)
    $(".cod_clickable").on('change', updateClickable)
    
})