fetch('/transactions/config/')
.then((result) => {return result.json();})
.then((data) => {
    const stripe = Stripe(`${data.publickKey}`);
    console.log(document.querySelector("#submit"))
    document.querySelector('#submit').addEventListener('click', () => {
        fetch('/transactions/create-checkout-session/')
        .then((result) => { return result.json(); })
        .then((data) => {
            console.log(data)
            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })

        .then((res) => {
            console.log(res);
        });
    });
});      
console.log('joera')
