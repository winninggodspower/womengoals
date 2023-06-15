<?php
// receiver email is gotten from command line argument => $argv[1]
// sender email is gotten from config.ini file

$config = parse_ini_file('config.ini');

if (count($argv) < 2) {
    echo "Please provide the recipient's email address as a command-line argument.";
    exit;
}

$from = $config['SENDER_EMAIL']
$to = $argv[1];
$subject = "Someone Volluntered To Womensgoal";
$message = "This is a test email.";

$headers = "From: $from\r\n";
$headers .= "Reply-To: $from\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/html; charset=ISO-8859-1\r\n";

if (mail($to, $subject, $message, $headers)) {
    echo "Email sent successfully!";
} else {
    echo "Email sending failed.";
}
?>
