// static/script.js
document.getElementById('iceBreakerForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    if (!name) {
        alert('Please enter a name.');
        return;
    }

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: name })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('summary').innerText = data.summary;
                document.getElementById('profilePic').src = data.profile_pic_url;
                document.getElementById('result').classList.remove('hidden');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
});