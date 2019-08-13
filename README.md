[Connexion]-based mockup service implementing parts of the [modified GA4GH Data Repository
Service API schema](mock_drs/specs/schema.data_repository_service.cd0186f.openapi.modified.yaml). The service was 
developed to implement and test [TEStribute],a task distribution logic package for TES instances. It features a 
mock DRS specification to provide parameters required for the model underlying the task distribution logic.

## Implementation

Note that only those parts of the service are implemented that are required for developing, testing and debugging 
[TEStribute](https://github.com/elixir-europe/TEStribute).
For all other endpoints only stubs are implemented that return the most basic valid response (typically an empty JSON 
object).

An important assumption that made during the deployment of this mock service is that the service assumes the 
consideration of the *object-id* field as a unique identifier across DRS instances. 

An original copy of the DRS schema will be available at all times [here](mock_drs/specs/schema.data_repository_service.cd0186f.openapi.yaml)
as a reference along with the [modified schema](mock_drs/specs/schema.data_repository_service.cd0186f.openapi.modified.yaml) which is used.

### The DRS Database

The DRS is populated with objects from the [../database/data_objects.json](mock_drs/database/data_objects.json) file 
and the id's of the objects that are loaded onto it need to be specified in the [../config/app_config.yaml](mock_drs/config/app_config.yaml) file. 
Only objects mentioned in the the [../database/data_objects.json](mock_drs/database/data_objects.json) file are available
to the DRS service. Again, the database relies on the uniqueness of the drs_id's of the objects.

## Usage

Once deployed and started (see below), the service is available here:
<http://localhost:9101/ga4gh/drs/v1/>

> Note that host and port may differ depending on the values specified in:
`mock_drs/config/app_config.yaml`
Explore the service via the Swagger UI:

```bash
firefox http://localhost:9101/ga4gh/drs/v1/ui/
```

Download/access the specs in JSON format:

```bash
wget http://localhost:9101/ga4gh/drs/v1/swagger.json
```

You can use the DRS client [DRS-cli](https://github.com/elixir-europe/DRS-cli) to send requests to the service.

## Deployment

### Dockerized

> "Production-like" containerized deployment without HTTP server/load balancer etc.
#### Requirements

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (tested with version 2.17.1)
- [Docker](https://docs.docker.com/install/) (tested with version 18.09.6)
- [docker-compose](https://docs.docker.com/compose/install/) (tested with version 1.24.0)

#### Building & starting the service

```bash
# Build application image
# [NOTE] Image re-building is not always necessary. Inspect the `Dockerfile`
#        to check which changes will need re-building.
docker-compose build
# Start service
docker-compose up -d
```

#### Other useful commands

```bash
# Check logs
docker-compose logs
# Shut down service
docker-compose down
```

### Non-dockerized

> Deployment for local development without containers, HTTP server/load balancer etc.
> Does **not** require Nginx or any certificates (HTTP only).
#### Requirements

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (tested with version 2.17.1)
- [Python](https://www.python.org/downloads/) (tested with versions 2.7.15+ & 3.6.8)
- [pip](https://pip.pypa.io/en/stable/installing/) (tested with version 19.1.1)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) (tested with version 15.1.0)

#### Installing & starting the service

```bash
# Clone repository
git clone git@github.com:elixir-europe/mock-DRS.git
cd mock-DRS
# Set up Python virtual environment
virtualenv -p `which python3` venv
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Install app
python setup.py develop
# Run service
python mock_drs/Server.py
```
*Note* you will also need to change the config file to support this by modifying the mongodb port from ```mongo``` to 
```localhost```


[Connexion]:https://github.com/zalando/connexion
[TEStribute]:https://github.com/elixir-europe/TEStribute
