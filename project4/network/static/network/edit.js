//Script to edit post and update without reload

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', editPost);
    })
})

function editPost(event){
    //Get post content
    const postDiv = event.target.parentNode.parentNode;
    const postContent = postDiv.querySelector('.post-content');

    //Create textarea element, populate with post content, and replace
    const editTextArea = document.createElement('textarea');
    editTextArea.textContent = postContent.textContent;
    editTextArea.classList.add('post-content')
    postContent.replaceWith(editTextArea);

    //Replace Edit button with Save button
    const saveButton = document.createElement('button');
    saveButton.classList.add('button-style');
    saveButton.classList.add('save-button');
    saveButton.textContent = 'Save';
    const editButton = event.target;
    editButton.replaceWith(saveButton);

    saveButton.addEventListener('click', () =>{
        //Update content in backend
        fetch('/post', { 
            method: 'PUT',
            body: JSON.stringify({
                id: postDiv.querySelector('.id').textContent,
                body: editTextArea.value
            })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });

        //Replace textarea with updated text
        postContent.textContent = editTextArea.value;
        editTextArea.replaceWith(postContent);

        //Replace save button with Edit Button
        saveButton.replaceWith(editButton);

    });
    
}


