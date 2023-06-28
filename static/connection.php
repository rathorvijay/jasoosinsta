<?php
$server="localhost:3307";
$user="root";
$password="";
$db="instagram-feedback";
$conn=mysqli_connect($server,$user,$password,$db);
if(!$conn)
echo "fail connection";
?>