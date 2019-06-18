"""
Mock Service for the GA4GH Data Repository Schema 
"""
import logging 

from connexion.resolver import RestyResolver
from connexion import App

app = App(__name__)
app.add_api('specs/schema.data_repository_service.cd0186f.openapi.modified.yaml')

if __name__ ==  '__main__' :
    app.run(host='0.0.0.0', port=5000, debug=True)
