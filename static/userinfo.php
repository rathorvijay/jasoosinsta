<?php
include 'connection.php';
// Get the JSON data from the HTTP request and decode it into a PHP object
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the JSON data from the HTTP request and decode it into a PHP object
    // $data = json_decode(file_get_contents('php://input'));
    $data = json_decode(file_get_contents('php://input'), true);
    if (!empty($data)) {
    $Username =$data->username;
    $Fullname=$data->fullname;
    $Description =$data->description;
    $externalUrl=$data->externalUrl;
    $profilepic = $data->profilepic;
    $private=$data->private;
    $posts = $data->posts;
    $followers=$data->followers;
    $follow=$data->follow;
    $insertdata="insert into userinfo(Username,Fullname,Description,ExternalUrl,Profilepic,Private,Posts,Followers,Follow)values('$Username','$Fullname','$Description','$externalUrl','$profilepic',' $private',' $posts',' $followers','$follow')";
    mysqli_query($conn,$insertdata);
}
}
?> 

