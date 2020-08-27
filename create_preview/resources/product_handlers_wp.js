jQuery(function($){
    $(document).ready(function() {
        if($("body.postid-8388").length){
            let preview_pic = $(".woocommerce-product-gallery__image")
        
        let customization_form = $("div.form-row")

        customization_form.append(`<button id="show_preview"> Show Preview </button>`)
        let show_preview = $("#show_preview")

        let getAttributeFromSelect = function(object) {
            let selected = object.children().filter(function(){
                return $(this).attr("selected") === "selected"
            })

            return selected.length > 0 ? $(selected[0]).data("optionid") : ["None"]
        }

        show_preview.click(function(e) {
            e.preventDefault()
            let data_content = [
                {
                    "name": "fonts",
                    "value": getAttributeFromSelect($("#font_type"))
                },
                {
                    "name": "paper_type",
                    "value": $($("#attribute_pa_select-paper-size").children("li.selected")[0]).data("value")
                },
                {
                    "name": "paper_stock",
                    "value": $($("#attribute_pa_select-paper-stock").children("li.selected")[0]).data("value")
                },
                {
                    "name": "alignment",
                    "value": getAttributeFromSelect($("#alignment"))
                },
                {
                    "name": "text_color",
                    "value": getAttributeFromSelect($("#text_color"))
                },
                {
                    "name": "quantity",
                    "value": parseInt($($("#attribute_pa_select-quantity").children("li.selected")[0]).data("value").split("-")[0])
                },
                {
                    "name": "line1",
                    "value": $("#line1").val()
                },
                {
                    "name": "line2",
                    "value": $("#line2").val()
                },
                {
                    "name": "line3",
                    "value": $("#line3").val()
                },
                {
                    "name": "line4",
                    "value": $("#line4").val()
                },
            ]
            let data_payload = {
                "font_type": data_content.filter((e) => {return e.name == "fonts"})[0].value,
                "paper_type": data_content.filter((e) => {return e.name == "paper_type"})[0].value,
                "paper_color": data_content.filter((e) => {return e.name == "paper_stock"})[0].value,
                "alignment": data_content.filter((e) => {return e.name =="alignment"})[0].value,
                "text_color": data_content.filter((e) => {return e.name == "text_color"})[0].value,
                "quantity": data_content.filter((e) => {return e.name == "quantity"})[0].value,
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
            let element_html = `<div class="woocommerce-product-gallery__image"><img src="" id="FeaturedMedia-pp-preview-pic" class="wp-post-image" width="400" height="510"></div>`
            // Get the photo from server
            $.ajax({
                type:"GET",
                url: "https://pp-custom-stationary-preview.herokuapp.com/generate-image?json="+encodeURIComponent(JSON.stringify(data_payload)),
                success: function(returned_data){
                    console.log(returned_data)
                    if($("#FeaturedMedia-pp-preview-pic").length){
                        $("#FeaturedMedia-pp-preview-pic").attr('src', returned_data)
                    } else {
                        preview_pic.children().css("display", "none")
                        preview_pic.append(element_html)
                        $("#FeaturedMedia-pp-preview-pic").attr('src', returned_data)
                    }
                }
            }).done(function(){

            }).fail(function() {
                alert("There was an error generating a preview. Please try again.")
            }).always(function(){
            })
        }
        }
        
        let paper_type_conv = function(paper_type){
            switch(paper_type){
                case "oxfordcream": return "oxford_creme";
                case "oxfordwhite": return "oxford_white";
                case "rivessand": return "rives_sand";
                case "riveswheat": return "rives_wheat";
                case "riveswhite": return "rives_white";
                case "speckletone": return "speckletone";
                case "superfinewhite": return "superfine_white";
            }
        }
    })
})