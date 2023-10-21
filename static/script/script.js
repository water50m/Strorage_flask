document.addEventListener('DOMContentLoaded', function(){ 
    const logregBox = document.querySelector('.logreg-box');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const forgetPLink = document.querySelector('.forgetP-link');
    const FloginLink = document.querySelector('.login-link-F');
    const FregisterLink = document.querySelector('.register-link-F');


    registerLink.addEventListener('click',()=>{
        logregBox.classList.add('activeR');
        
    })

    forgetPLink.addEventListener('click',() =>{
        logregBox.classList.add('activeF');
    })


    loginLink.addEventListener('click',()=>{
        logregBox.classList.remove('activeR');
    })

    FloginLink.addEventListener('click',() =>{
        logregBox.classList.remove('activeF');
    })   
    
    FregisterLink.addEventListener('click',() =>{
        logregBox.classList.add('activeR');
        logregBox.classList.remove('activeF');
    })

    const params = new URLSearchParams(window.location.search);
    if (params.get('showRegister') === 'true') {
        logregBox.classList.add('activeR');
    }
});
// document.addEventListener('DOMContentLoaded', function(){  
//     const logregBox = document.querySelector('.logreg-box');
//     const loginLink = document.querySelector('.login-link');
//     const registerLink = document.querySelector('.login-register');

//     registerLink.addEventListener('click', () => {
//         logregBox.classList.add('active');
//     });

//     loginLink.addEventListener('click', () => {
//         logregBox.classList.remove('active');
//     });

//     // Check URL parameters
//     const params = new URLSearchParams(window.location.search);
//     if (params.get('showRegister') === 'true') {
//         logregBox.classList.add('active');
//     }
// });





