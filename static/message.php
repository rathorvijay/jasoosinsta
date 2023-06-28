<?php
include 'connection.php';

if (isset($_POST["submit"])) 
{
    $name = $_POST["name"];
    $email = mysqli_real_escape_string($conn, $_POST["email"]);
    $subject = $_POST["subject"];
    $massage = $_POST["massage"];
    $insertdata= " insert into feedback(name,email,subject,massage)values('$name','$email','$subject','$massage')";
            $queryrun= mysqli_query($conn,$insertdata);
            if($queryrun)
            {
            ?>
                <script>
                   var v=alert("feedback submit successfully");
                   location.replace("../index.html");
                   
                </script>
                <?php
            }
            else
            { ?>
                <script>
                    alert("something went wrong insert");
                </script>
                <?php
            }
}
?>


