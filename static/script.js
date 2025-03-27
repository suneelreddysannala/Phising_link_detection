document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const urlInput = document.getElementById('urlInput').value;
    fetch('http://localhost:5000/classify-url/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = 'Classification: ' + data.classification;
    })
    .catch(error => console.error('Error:', error));
});
