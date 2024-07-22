
var fav_but = document.getElementsByClassName("favourite-button")
var manage_but = document.getElementsByClassName("manage-button")
const sum_list = [...fav_but, ...manage_but]

console.log(sum_list)
// for (let i=0;i < fav_but.length; i+=1){
//     fav_but[i].addEventListener('click',function(){
//         var is = this.querySelector("i")
//         if(is.classList.contains("fa-regular")){
//             is.className = 'fa-solid fa-heart'
//         }else{
//             is.className = 'fa-regular fa-heart'
//         }
//     })
// }


for (var i = 0;i <sum_list.length;i++){
    sum_list[i].addEventListener("click",function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId,action)



        console.log('USER',user)
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
    console.log('URL:', url)



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

    .then((data)=>{
        console.log('data:',data)
    })

}

consoleText(["There is nothing actually","Just air"],"text",["black","blue"])
function consoleText(words,id,colors){
    if(colors==undefined) colors=["fff"];
    var visible=true;
    var con=document.getElementById("console");
    var letterCount=1;
    var x=1;
    var waiting=false;
    var target=document.getElementById(id);
    var stoptimer=0;
    target.setAttribute("style","color:"+colors[0])
    const megashow=setInterval(shows,120)
    function shows(){
        if(letterCount=== 0 && waiting===false){
            waiting=true;
            target.innerHTML=words[0].substring(0,letterCount)
            window.setTimeout(function(){
                var usedColor=colors.shift();
                colors.push(usedColor);
                var usedWord=words.shift();
                words.push(usedWord);
                x=1;
                target.setAttribute("style","color:"+ colors[0])
                letterCount+=x;
                waiting=false
            },1000)
        }
        else if(letterCount===words[0].length+1 && waiting===false){
            waiting=true;
            window.setTimeout(function(){
                x= -1;
                letterCount +=x;
                waiting=false;
            },1000)
        }
        else if(waiting===false){
            target.innerHTML =words[0].substring(0,letterCount)
            letterCount+=x
        }
    }
    window.setInterval(function() {
        if (visible === true) {
          con.className = 'console-underscore hidden'
          visible = false;
    
        } else {
          con.className = 'console-underscore'
    
          visible = true;
        }
      }, 400)    
}


