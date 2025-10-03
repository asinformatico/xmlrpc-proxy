<?php
class WordPressXMLRPCProxy {
    private $wordpress_url;
    private $username;
    private $password;
    
    public function __construct($wordpress_url, $username, $password) {
        $this->wordpress_url = $wordpress_url . '/xmlrpc.php';
        $this->username = $username;
        $this->password = $password;
    }
    
    public function makeProxyRequest($target_url) {
        // Obtener contenido de la URL objetivo
        $target_content = file_get_contents($target_url);
        $encoded_content = base64_encode($target_content);
        
        // Construir solicitud XML-RPC
        $xml_request = '<?xml version="1.0" encoding="utf-8"?>
<methodCall>
    <methodName>wp.newPost</methodName>
    <params>
        <param><value><string>1</string></value></param>
        <param><value><string>' . $this->username . '</string></value></param>
        <param><value><string>' . $this->password . '</string></value></param>
        <param>
            <value>
                <struct>
                    <member>
                        <name>post_title</name>
                        <value><string>Proxy Content</string></value>
                    </member>
                    <member>
                        <name>post_content</name>
                        <value><string>' . $encoded_content . '</string></value>
                    </member>
                    <member>
                        <name>post_status</name>
                        <value><string>draft</string></value>
                    </member>
                </struct>
            </value>
        </param>
    </params>
</methodCall>';
        
        // Enviar solicitud
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->wordpress_url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $xml_request);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/xml',
            'User-Agent: WordPress Proxy Client'
        ));
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return $response;
    }
}

// Ejemplo de uso
$proxy = new WordPressXMLRPCProxy(
    'http://localhost/wordpress',
    'admin', 
    'admin123'
);

$result = $proxy->makeProxyRequest('http://192.168.1.100/internal-dashboard');
echo $result;
?>
