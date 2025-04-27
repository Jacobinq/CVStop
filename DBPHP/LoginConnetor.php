<?php
session_start(); 
include 'connect.php'; 

$email = $_POST['email'];
$password = $_POST['password'];

$sql = "SELECT * FROM users WHERE email = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();
$user = $result->fetch_assoc();

if ($user) {
    if (password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['name'];
        header("Location: /CVStop/Home.html"); 
        exit();
    } else {
        echo "Incorrect password.";
    }
} else {
    echo "No user found with that email.";
}


$conn->close();
?>