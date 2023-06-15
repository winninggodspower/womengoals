<?php
// subject email message is gotten from command line argument => $argv[1]
// receiver and sender email is gotten from config.ini file

$config = parse_ini_file('config.ini');

if (count($argv) < 3) {
    echo "Please provide the email message as command-line arguments.";
    exit;
}

$to = $config['RECEIVER_EMAIL'];
$from = $config['SENDER_EMAIL'];
$subject =  $argv[1];
$message = $argv[2];

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