import requests

def check_xmlrpc_enabled(wordpress_url):
    """
    Verifica si xmlrpc.php está habilitado en un sitio WordPress
    """
    xmlrpc_url = wordpress_url.rstrip('/') + '/xmlrpc.php'
    
    # Método 1: Verificar acceso directo
    try:
        response = requests.get(xmlrpc_url, timeout=5)
        if response.status_code == 200 and 'XML-RPC server accepts POST requests only' in response.text:
            return True, "XML-RPC habilitado"
    except:
        pass
    
    # Método 2: Verificar mediante pingback
    pingback_payload = """<?xml version="1.0" encoding="utf-8"?>
<methodCall>
    <methodName>system.listMethods</methodName>
    <params></params>
</methodCall>"""
    
    try:
        response = requests.post(xmlrpc_url, data=pingback_payload, timeout=5)
        if response.status_code == 200 and 'pingback' in response.text.lower():
            return True, "Pingback habilitado - VULNERABLE"
    except:
        pass
    
    return False, "XML-RPC parece deshabilitado"

# Escanear múltiples sitios
sites_to_check = [
    'http://sitio1.com',
    'http://sitio2.com',
    'http://sitio3.com'
]

for site in sites_to_check:
    enabled, message = check_xmlrpc_enabled(site)
    print(f"{site}: {message}")
