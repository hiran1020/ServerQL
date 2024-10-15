


//mAIN PAGE
// Auto hide alert after 5 seconds
setTimeout(function() {
    document.getElementById('alert-message').style.display = 'none';
}, 5000); // 5 seconds

// Close alert manually
document.querySelector('.alert-box .close').addEventListener('click', function() {
    document.getElementById('alert-message').style.display = 'none';
});

// Helper function to check if the input is a phone number
function isPhoneNumber(input) {
    return /^\d+$/.test(input);
}

// Form submission with validations, +1 prefix for phone numbers, and loader
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const phoneNumber = document.getElementById("phone_number").value;
    const password = document.getElementById("password").value;
    const serverName = document.getElementById("server_name").value;

    // Validate that all fields are filled
    if (!phoneNumber || !password || !serverName) {
        alert("Please fill in all fields.");
        return false;
    }

    // If the input is all digits, treat it as a phone number and add +1
    if (isPhoneNumber(phoneNumber)) {
        if (!phoneNumber.startsWith('+1')) {
            document.getElementById('phone_number').value = '+1' + phoneNumber;
        }
    }

    // Show loader and disable form
    document.getElementById('loader').style.display = 'block';
    document.querySelector('.box').classList.add('loading');
    document.querySelector('.submit').disabled = true;

    // Simulate login request (Replace this part with actual AJAX login logic)
    setTimeout(function() {
        // Hide loader after receiving response
        document.getElementById('loader').style.display = 'none';
        document.querySelector('.box').classList.remove('loading');
        document.querySelector('.submit').disabled = false;

        // Simulate redirect (for example)
        window.location.href = "/dashboard"; // Change this URL as needed
    }, 25000); 
});




//DASHBOARD PAGE

