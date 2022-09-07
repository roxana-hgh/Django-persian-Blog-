document.addEventListener('DOMContentLoaded', () => {



    const hamberger = document.getElementById('hamberger')
    const navUl = document.getElementById('nav-menu')
    
    hamberger.addEventListener('click', () => {
        navUl.classList.toggle('show')
        hamberger.classList.toggle('active')
    })
    
    })
    
    const search_icon = document.getElementById('search-icon')
    const search_bar = document.getElementById('search-bar')
    
    search_icon.addEventListener('click', () => {
        search_bar.classList.toggle('show')
    })
    
    

    