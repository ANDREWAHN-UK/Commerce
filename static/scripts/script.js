

// need to use windows.onload otherwise it will not work :(
    // This function identifies the add to cart button has been clicked, and logs what the product id and user are
    // if the user is logged in, it executes updateUserOrder()
window.onload = function () {
    for (i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var productId = this.dataset.product
            var action = this.dataset.action
            console.log('productId:', productId, 'Action:', action)

            console.log('USER:', user)
		if (user == 'AnonymousUser'){
			console.log('User is not authenticated')
			
		}else{
			updateUserOrder(productId, action)
		}
        })
    }
}

var updateBtns = document.getElementsByClassName('update-cart')


// this function gets called above
// it fetches the function in the url
// the post request turns the product id and action as a json Object, and string formats it

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = 'update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}
