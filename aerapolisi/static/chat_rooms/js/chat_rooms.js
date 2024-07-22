let ext_but = document.querySelector('.extend-button')
let ext_content = document.querySelector('.seller-ownership')

let chat_window = document.querySelector('.chat')

ext_but.addEventListener('click', (e) => {
    console.log(ext_but.innerHTML)
    if(ext_but.value == 'unwrapped'){
        ext_content.style.transform = 'translateX(100%)'
        chat_window.style.width = '150vw'
        ext_but.innerHTML = '<<<'
        ext_but.value = 'wrapped'
    }else{
        ext_content.style.transform = 'translateX(0)'
        chat_window.style.width = '55vw'
        ext_but.innerHTML = '>>>'
        ext_but.value = 'unwrapped'
    }
})