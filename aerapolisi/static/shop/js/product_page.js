buts = document.querySelectorAll(".product-view__image-button")

for (let i=0;i < buts.length; i+=1){
    buts[i].addEventListener('click',function(){
        var is = this.querySelector(".product-view__image")
        var at = document.querySelector(".product-view__image--main")
        at.innerHTML = is.innerHTML
    })
}