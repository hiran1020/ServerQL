document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    const tenant = document.getElementById('tenant').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `phone=${encodeURIComponent(phone)}&password=${encodeURIComponent(password)}&tenant=${encodeURIComponent(tenant)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('loginForm').style.display = 'none';
            localStorage.setItem('authToken', data.token);
            alert('Login successful!');
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});