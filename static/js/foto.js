
  function previewFoto(event){
    const file = event.target.files[0];
    const preview = document.querySelector(".profile-pic");

    if (file){
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.style.backgroundImage = `url(${e.target.result})`;
            preview.style.backgroundSize = "cover";
            preview.style.backgroundPosition = "center";
        };
        reader.readAsDataURL(file);
  }
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("foto");
    input.addEventListener("change", previewFoto);
});
