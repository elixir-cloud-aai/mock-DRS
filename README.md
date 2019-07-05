[Connexion](https://github.com/zalando/connexion)-based mockup service implementing parts of the GA4GH Task Execution
Service API schema. The service was developed to implement and test [TEStribute](https://github.com/elixir-europe/TEStribute),
a task distribution logic package for TES instances. It features an extended
TES specification to provide parameters required for the model underlying the
task distribution logic.

## Implementation

Not that only those parts of the service are implemented that are required for
developing, testing and debugging [TEStribute](https://github.com/elixir-europe/TEStribute).
For all other endpoints only stubs are implemented that return the most basic
valid response (typically an empty JSON object).

### Modified DRS specs

Coming soon...

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