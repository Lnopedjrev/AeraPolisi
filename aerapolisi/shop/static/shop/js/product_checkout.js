let chnge_but = document.querySelector('#change_call')
let chnge_cont = document.querySelector(".data-change__container")
let but_clear = document.querySelectorAll('.clear-button')
let chnge_comm = document.querySelector("#change_submit")
let form = document.getElementById('change_ship-form')
let conf_but = document.querySelector("#confirm-button")
let final_form = document.getElementById('final-form')

console.log(but_clear)

chnge_but.addEventListener('click', function(e){
    console.log('sosai')
    chnge_cont.style.display = 'block'
})

conf_but.addEventListener('click', function(e){
    var new_ship_v = document.querySelectorAll('#new_ship-value')
    but_clear[1].parentElement.style.display = 'flex'
    for (let i=1;i < new_ship_v.length+1 ; i+=1){
        final_form[i].value = new_ship_v[i-1].innerHTML
    }

})

for (let i=0;i < but_clear.length; i+=1){
    but_clear[i].addEventListener('click', (e) =>{
        but_clear[i].parentElement.style.display = 'none'
    })
}

chnge_comm.addEventListener('click', function(e){
    var new_ship = [form.address.value, form.city.value, form.state.value, form.zipcode.value]
    let new_ship_v = document.querySelectorAll('#new_ship-value')
    console.log(new_ship_v)
    for (let i=0;i < new_ship_v.length; i+=1){
        new_ship_v[i].innerHTML = new_ship[i]
    }
    chnge_cont.style.display = 'none'
})