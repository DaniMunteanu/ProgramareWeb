var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i<updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function()
    {
        var stickerId = this.dataset.sticker
        var action = this.dataset.action
        console.log('stickerId:', stickerId, 'action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser')
            console.log('User is not authenticated')
        else
            updateUserOrder(stickerId, action)
    }
    )
}

function updateUserOrder(stickerId, action){
    console.log('User is authenticated, sending data...')

    var url = '/update_cart/'

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
        console.log('data:', data)
        location.reload()
    })

}
