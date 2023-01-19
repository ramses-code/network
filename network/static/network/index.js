document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#container').addEventListener('click', (e) => {
        if (e.target.matches('button')) {
            if (e.target.textContent === 'Edit') {
                let postId = e.target.parentNode.id;
                document.getElementById(postId).style.display = 'none';
                let divEditor = document.getElementById(`${postId}_editor`);
                divEditor.classList.remove('d-none');

                let edit = document.getElementById(`${postId}_edit`);
                edit.addEventListener('click', () => {
                    editPost(postId);
                    document.getElementById(postId).style.display = 'block';
                    divEditor.classList.add('d-none');
                });
            }
        } else if (e.target.matches('span')) {
            let div = e.target.parentNode;
            like(div.id);
        }
    });
});

function editPost(postId) {
    let post = document.getElementById(`${postId}_text`).value;
    
    fetch(`/post/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({
            post: post,
        })
    })
    .then(response => response.json())
    .then(post => {
        let div = document.getElementById(postId);
        div.querySelector('.post').innerHTML = post.post;
        div.querySelector('.timestamp').innerHTML = post.timestamp;
    })
}

function like(postId) {
    fetch(`/post/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({like: 'like'})
    })
    .then(response => response.json())
    .then(data => {
        let div = document.getElementById(postId);
        div.querySelector('.likes-count').innerHTML = data.likes;
    })
    .catch(err => err)
};
