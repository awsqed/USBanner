<form id="loginForm" action="/login.php" method="post">
    <table>
        <tr>
            <td><label for="txtUsername">Username: </label></td>
            <td><input id="txtUsername" type="text" name="txtUsername"></td>
        </tr>
        <tr>
            <td><label for="txtPassword">Password: </label></td>
            <td><input id="txtPassword" type="password" name="txtPassword"></td>
        </tr>
        <tr>
            <td></td>
            <td><input type="submit" name="btnSubmit" value="Login"></td>
        </tr>
    </table>
</form>

<?php

require_once('lib/WConfig.php');
require_once('lib/DBUtils.php');

$dbUtils = new DBUtils();
$dbUtils->connect(WConfig::$_DBHOST, WConfig::$_DBUSER, WConfig::$_DBPASS, WConfig::$_DB_NAME);
$dbUtils->select_db(WConfig::$_TABLE_NAME);

if (!isset($_POST['btnSubmit'])) {
    return;
}

if (!isset($_POST['txtUsername']) || empty($_POST['txtUsername'])) {
    echo "Username can't be empty.";
    return;
}

if (!isset($_POST['txtPassword']) || empty($_POST['txtPassword'])) {
    echo "Password can't be empty.";
    return;
}

$username = $_POST['txtUsername'];
$password = $_POST['txtPassword'];
if ($dbUtils->verify_password($username, $password)) echo 'Logged in.';
else echo 'Invalid account credential.';

?>