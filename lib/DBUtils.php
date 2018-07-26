<?php

class DBUtils {

    private $conn;

    public function connect($dbhost, $dbusername, $dbpassword, $dbname) {
        $this->conn = new mysqli($dbhost, $dbusername, $dbpassword, $dbname);
        if ($this->conn->connect_error) {
            die("Connection Error (" . $this->conn->connect_errno . '): ' . $this->conn->connect_error);
        }
    }

    public function select_db($newdb) {
        $this->conn->select_db($newdb);
    }

    private function query($query, $type, $params) {
        $smtp = $this->conn->prepare($query);
        call_user_func_array(array($smtp, 'bind_param'), array_merge(array($type), $params));
        $result = $smtp->execute();
        $data = $smtp->get_result();
        $smtp->close();
        $result_arr = array();
        if (!is_bool($data)) {
            while ($single_result = $data->fetch_array(MYSQLI_NUM))
                $result_arr[] = $single_result;
        }
        return $data ? $result_arr : $result;
    }

    public function has_account($username) {
        $result = $this->query("SELECT id FROM user_accounts WHERE username = ?", 's', array(&$username));
        return isset($result[0]);
    }

    public function get_password($username) {
        $username = $this->conn->real_escape_string($username);
        $result = $this->query("SELECT password FROM user_accounts WHERE `username` = ?", 's', array(&$username));
        return $this->has_account($username) ? $result[0][0] : "";
    }

    public function verify_password($username, $password) {
        $username = $this->conn->real_escape_string($username);
        $hashedPassword = $this->get_password($username);
        return hash('md5', $password) == $hashedPassword;
    }

    public function __destruct() {
        if ($this->conn) $this->conn->close();
    }

}

?>