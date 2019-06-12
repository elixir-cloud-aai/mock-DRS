"""
Mock Service for the GA4GH Data Repository Schema 
"""
from connexion.resolver import RestyResolver
import connexion

app.add_api('schema.data_repository_service.cd0186f.openapi.modified.yaml')

if __name__ ==  '__main__' :
    app.run(host='0.0.0.0', port=5000, debug=True)


# from connexion import App
# app = App(__name__)
# app.add_api('specs/schema.data_repository_service.cd0186f.openapi.modified.yaml')

