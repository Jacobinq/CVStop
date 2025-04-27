<?php
session_start(); // Start a new session

include 'connect.php'; // Connect to the database

// Get form input
$email = $_POST['email'];
$password = $_POST['password'];

// Find user by email
$sql = "SELECT * FROM users WHERE email = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();
$user = $result->fetch_assoc();

if ($user) {
    // Verify password
    if (password_verify($password, $user['password'])) {
        // Password correct, log user in
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['name'];
        header("Location: dashboard.php"); // Redirect to a dashboard page
        exit();
    } else {
        echo "Incorrect password.";
    }
} else {
    echo "No user found with that email.";
}

$conn->close();
?>