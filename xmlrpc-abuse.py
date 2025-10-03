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
</methodCall>"""
        
        headers = {
            'Content-Type': 'application/xml',
            'User-Agent': 'WordPress Proxy Client'
        }
        
        # Enviamos la solicitud a xmlrpc.php
        proxy_response = requests.post(self.wordpress_url, data=xml_payload, headers=headers)
        return proxy_response.text

# Uso del script
if __name__ == "__main__":
    # Configuración (¡ESTOS DATOS DEBEN SER VÁLIDOS!)
    wp_url = "http://tusitio-wordpress.com"
    username = "admin"
    password = "password123"
    target_url = "http://sitio-interno.com/info-confidencial"
    
    proxy = WordPressProxy(wp_url, username, password)
    result = proxy.make_proxy_request(target_url)
    print("Respuesta del proxy:", result)
