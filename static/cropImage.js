const imageBox = document.querySelector("#image_box");
const imageForm = document.querySelector("#image_form");
const uploadBtn = document.querySelector(".confirm-btn");
const imageInput = document.querySelector("#coin_image");
const labelUpload = document.querySelector("#upload_label");

const csrf = document.getElementsByName("csrf_token");
const imageName = "my_image_" + new Date().toJSON().slice(0, 18).replaceAll(":", "_")+".jpg" // for file naming


imageInput.addEventListener("change", ()=>{
    // uploadBtn.classList.remove("not-visible");
    // labelUpload.classList.add("not-visible");

    const img_data = imageInput.files[0];
    console.log(img_data)
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="coin-image" style="max-width:500px; max-height:500px;">`;
    let $image = $("#coin-image");

    $image.cropper({
        aspectRatio: 9/16,
        viewMode: 3, // Important! Image fills container
    })

    let cropper = $image.data("cropper");
    uploadBtn.addEventListener("click", ()=>{
        cropper.getCroppedCanvas().toBlob((blob) => {
            let fd = new FormData()
            // saveBlob(blob, imageName)
            fd.append("coin_image", blob, imageName); //model img variable name
            fd.append("csrf_token", csrf[0].value);
            console.log(blob)
            $.ajax({
                type: "POST",
                url: imageForm.action,
                enctype: "multipart/form-data",
                data:fd,
                cache:false,
                contentType: false,
                processData:false,
            })
        })
    })
})



