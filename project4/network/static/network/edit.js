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
    event.target.replaceWith(saveButton);

    saveButton.addEventListener('click', () =>{
        console.log('TO SAVE AND UPDATE');
    })
    
}