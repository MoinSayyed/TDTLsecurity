<?php
$uname = $_GET['uname'];
$pwd = $_GET['pwd'];
$servername = "localhost";
$username = "root";
$conn = new sqli($servername, $username, $password, 'test');

if ($conn -> connect_error){
    die("Connection Failed : " . $conn -> connect_error);
}

$sql = "SELECT * FROM login_details WHERE username = '$uname' AND password =  '$pwd'";
$result = mysqli_query($conn, $sql);
$check = mysqli_fetch_array($result);

if(isset($check)){
    echo 'Login Success :)';
}else{
    echo 'Login Faliure :(';
}
?>