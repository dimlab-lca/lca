#!/usr/bin/python3.9
"""
LCA TV Application Entry Point for PlanetHoster/cPanel
Domain: lca-tv.bf (root domain deployment)
Compatible with Passenger WSGI
"""

import os
import sys

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def app(environ, start_response):
    """WSGI application entry point for LCA TV - Root Domain"""
    try:
        # Ensure proper URL scheme
        if 'HTTP_X_FORWARDED_PROTO' in environ:
            environ['wsgi.url_scheme'] = environ['HTTP_X_FORWARDED_PROTO']
        elif environ.get('HTTPS', '').lower() in ('on', '1'):
            environ['wsgi.url_scheme'] = 'https'
        
        # Import and run the Flask app
        from app import application as flask_app
        return flask_app(environ, start_response)
        
    except ImportError as e:
        # If import fails, return a detailed error page
        error_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <title>LCA TV - Erreur d'importation</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .error {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .error h1 {{ color: #dc3545; }}
        .error pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }}
        .info {{ margin-top: 20px; padding: 15px; background: #e9ecef; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="error">
        <h1>LCA TV - Erreur d'importation</h1>
        <p><strong>Erreur:</strong> {str(e)}</p>
        
        <div class="info">
            <h3>Informations de débogage:</h3>
            <p><strong>Version Python:</strong> {sys.version}</p>
            <p><strong>Répertoire actuel:</strong> {os.getcwd()}</p>
            <p><strong>Fichiers dans le répertoire:</strong></p>
            <pre>{chr(10).join(os.listdir(os.path.dirname(__file__) or '.'))}</pre>
        </div>
        
        <div class="info">
            <h3>Étapes de dépannage:</h3>
            <ol>
                <li>Vérifier que tous les fichiers Python sont téléchargés correctement</li>
                <li>Vérifier que app.py existe dans le répertoire de l'application</li>
                <li>Vérifier les dépendances Python: pip install -r requirements.txt</li>
                <li>Vérifier les permissions des fichiers (755 pour les répertoires, 644 pour les fichiers)</li>
                <li>Redémarrer l'application dans cPanel</li>
            </ol>
        </div>
    </div>
</body>
</html>
        """
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_html.encode('utf-8')]
        
    except Exception as e:
        # Handle any other errors
        import traceback
        error_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <title>LCA TV - Erreur d'application</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .error {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .error h1 {{ color: #dc3545; }}
        .error pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="error">
        <h1>LCA TV - Erreur d'application</h1>
        <p><strong>Erreur:</strong> {str(e)}</p>
        
        <p><strong>Traceback:</strong></p>
        <pre>{traceback.format_exc()}</pre>
        
        <p><strong>Version Python:</strong> {sys.version}</p>
        <p><strong>Horodatage:</strong> {__import__('datetime').datetime.now()}</p>
    </div>
</body>
</html>
        """
        
        start_response('500 Internal Server Error', [('Content-Type', 'text/html; charset=utf-8')])
        return [error_html.encode('utf-8')]
