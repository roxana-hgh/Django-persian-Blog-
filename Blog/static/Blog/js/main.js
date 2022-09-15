document.addEventListener('DOMContentLoaded', () => {



    const hamberger = document.getElementById('hamberger')
    const navUl = document.getElementById('nav-menu')
    
    hamberger.addEventListener('click', () => {
        navUl.classList.toggle('show')
        hamberger.classList.toggle('active')
    })
    
    })
    
   
    
    

    