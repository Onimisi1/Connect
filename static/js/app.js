
    // To get the search form and pagination links

    let searchForm = document.getElementById('searchForm')
    let pageLinks = document.getElementsByClassName('icon-style')

    // Check search form exist

    if(searchForm){
        for(let i=0; pageLinks.length > i; i++){
            pageLinks[i].addEventListener('click', function (e) {
                e.preventDefault()

                // Now to get the data attribute

                let page = this.dataset.page
                console.log('PAGE:', page)

                // add a hidden search input to form

                searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

                // Submit form
                searchForm.submit()
            })
        }
    }




document.addEventListener('DOMContentLoaded', function () {
    h1js.highlightAll();
});


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
    console.log('Alert Wrapper clicked')
    alertClose.addEventListener('click', () =>
        alertWrapper.style.display = 'none'
    )
}