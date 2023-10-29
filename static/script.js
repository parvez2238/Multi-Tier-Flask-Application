document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(event.target);

    // Clear previous response messages
    const responseElement = document.getElementById('response');
    responseElement.textContent = '';

    // Send a POST request to the server
    fetch('/api/save', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // Check if the response is successful (status code 200)
        if (response.ok) {
            return response.json();
        }
        // If there's an error, throw it and catch it in the next `catch` block
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Display success message from the server response
        responseElement.textContent = data.message;

        // Clear form fields after successful submission
        document.getElementById('name').value = '';
        document.getElementById('email').value = '';
    })
    .catch(error => {
        // Display error message in case of network issues or server errors
        responseElement.textContent = 'An error occurred while processing your request.';
        console.error('Error:', error);
    });
});

// Fetch data from the server
fetch('/api/data')
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Select the data container
        const dataContainer = document.getElementById('data-container');

        // Iterate through the data and create card elements
        data.forEach(item => {
            // Create a new card element
            const card = document.createElement('div');
            card.className = 'card';
            
            // Populate card content with data from the server
            card.innerHTML = `
                <h2>${item.name}</h2>
                <p>Email: ${item.email}</p>
            `;
            
            // Append the card to the data container
            dataContainer.appendChild(card);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
