document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('#add-post').addEventListener('click', addPost);


    function addPost(){
        

        // Get value from textarea
        postContent = document.getElementById('new-post-text').value
        
        // Send POST request to /post
        fetch('/post', {
            method: 'POST',
            body: JSON.stringify({
              content: postContent
            })
          })
          .then(response => response.json())
          .then(result => {
            console.log(result);
          });
    }
})
