document.addEventListener('mousemove',e => {
    Object.assign(document.documentElement, {
        style: `
        --move-x:${(e.clientX - window.innerWidth / 2)  * -.001}deg;
        --move-y:${(e.clientY - window.innerHeight / 2) * -.001}deg;
        `
    })
})


var fav_but = document.getElementsByClassName("favourite-button")
var manage_but = document.getElementsByClassName("manage-button")
const sum_list = [...fav_but, ...manage_but]


for (var i = 0;i < sum_list.length; i++){
    sum_list[i].addEventListener("click",function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        if(user === 'AnonymousUser'){
            console.log("Not logged in")
        }else{
            updateUserOrder(productId,action)
        }
        if (this.id === 'favourite-add'){
            this.nextElementSibling.style.display = "block"
            this.style.display = "none"
        }else{
            this.previousElementSibling.style.display = "block"
            this.style.display = "none"
        }
        if (action=='approve'|| action=='decline'){
            location.reload()
        }
    })

}

function updateUserOrder(productId,action){
    var url = '/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

}