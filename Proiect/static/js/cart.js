var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i<updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function()
    {
        var stickerId = this.dataset.sticker
        var action = this.dataset.action
        console.Log('stickerId:', stickerId, 'action:', action)

        console.Log('USER:', user)
        if(user == 'AnonymousUser')
            console.Log('User is not authenticated')
        else
            updateUserOrder(stickerId, action)
    }
    )
}

function updateUserOrder(productId, action){
    console.Log('User is authenticated, sending data...')

    var url = '/update_sticker/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'stickerId': stickerId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })

}
