//Script to like posts

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', like);
    })
})

function like(event){
    //Get post parent
    const likeButton = event.target;
    const postDiv = likeButton.parentNode.parentNode.parentNode;
    
    //Update likes in backend
    fetch('/like', { 
        method: 'PUT',
        body: JSON.stringify({
            id: postDiv.querySelector('.id').textContent  
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result['message']);
            const likes = postDiv.querySelector('.likes > span');
            likes.innerText = result['likes'];
        });
}
