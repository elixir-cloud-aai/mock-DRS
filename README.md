# mock-DRS
[Connexion]-based mockup service implementing parts of the GA4GH [Data Repository
Service] (DRS) API schema. The service was developed to implement and test
[TEStribute], a task distribution logic package for TES instances. It features
an [extended TES specification] to provide parameters required for the model
underlying the task distribution logic.

## Usage

Once deployed and started ([see below](#Deployment)), the service is available here:
<http://localhost:9101/ga4gh/drs/v1/>

You can explore the service via the Swagger UI:

```bash
firefox http://localhost:9101/ga4gh/drs/v1/ui/
```

The specifications, in JSON format, can be retrieved with:

```bash
wget http://localhost:9101/ga4gh/drs/v1/swagger.json
```

> Note that host and port can be set manually in the [config] file. In that
> case, the values in the URLs above need to be replaced as well.

The client [DRS-cli] to send requests to the service.

 
## Deployment

`mock-DRS` can be deployed via containers (preferred) or after manual
installation of all dependencies.

In both cases, the repository first needs to be cloned with:

```bash
git clone git@github.com:elixir-europe/mock-DRS.git
```
Afterwards traverse to the repository's root directory with :

```bash
cd mock-DRS
```

### Containerised Deployment 
> "Production-like" containerized deployment without HTTP server/load balancer
> etc.

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

> Deployment for local development without containers, HTTP server/load
> balancer etc.

#### Requirements

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (tested with version 2.17.1)
- [Python](https://www.python.org/downloads/) (tested with versions 2.7.15+ & 3.6.8)
- [pip](https://pip.pypa.io/en/stable/installing/) (tested with version 19.1.1)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) (tested with version 15.1.0)

#### Installing & starting the service

```bash
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
*Note* you will also need to change the config file to support this by modifying the mongodb port
 from ```mongo``` to ```localhost```

## Implementation details 

Note that only those parts of the service are implemented that are required for developing, testing 
and debugging [TEStribute]. For all other endpoints only stubs are implemented that return 
the most basic valid response (typically an empty JSON object).

An important assumption that made during the deployment of this mock service is that the service
 assumes the consideration of the *object-id* field as a unique identifier across DRS instances. 

An original copy of the DRS schema will be available at all times 
[here](mock_drs/specs/schema.data_repository_service.cd0186f.openapi.yaml) as a reference along 
with the [modified schema](mock_drs/specs/schema.data_repository_service.cd0186f.openapi.modified.yaml)
 which is used.

### The DRS Database

The DRS is populated with objects from the [../database/data_objects.json](mock_drs/database/data_objects.json) file 
and the id's of the objects that are loaded onto it need to be specified in the 
[../config/app_config.yaml](mock_drs/config/app_config.yaml) file. Only objects mentioned in the 
[../database/data_objects.json](mock_drs/database/data_objects.json) file are available to the DRS
 service. Again, the database relies on the uniqueness of the drs_id's of the objects.


#### Database configuration

The database can be configured with different data objects **if** their corresponding
data objects are present in the [../database/data_objects.json](mock_drs/database/data_objects.json) 
file. Default objects `database` section of the service's [config] and they
can be edited by the user before starting the service.

Alternatively (and preferably), these objects can be modified in the running
service via the `/update-db` endpoint, which is particularly useful for
setting up environments for various testing scenarios for [TEStribute]. The
endpoint is defined in the [config specifications]:

```yaml
    /update-db:
    post:
      summary: Object id's in the array that need to be added to the db
      operationId: updateDatabaseObjects
      consumes:
        - application/json
      produces:
        - application/json
      parameters:
        - name: body
          in: body
          description: ''
          schema:
            $ref: '#/definitions/UpdateObjects'
          required: true
      responses:
        200:
          description: "200 response"
          schema:
              $ref: '#/definitions/UpdateObjects'
      tags:
        - DataRepositoryService
      x-swagger-router-controller: ga4gh.drs.server
```

It relies on the following models:

```yaml
  UpdateObjects:
    type: object
    properties:
      clear:
        type: boolean
      objects:
        type: array
        items:
          type: string
```
[DRS-cli] can be used to update the task info parameters.

> Note that while the `/update-db` endpoint can be accessed via the same
> root URI (and explored via the Swagger UI), it was not included in the
> [modified DRS specifications], but rather added to it _on the fly_ when the
> service is started.

## Contributing

This project is a community effort and lives off your contributions, be it in
the form of bug reports, feature requests, discussions, or fixes and other code
changes. Please read the [contributing guidelines] if you want to contribute.
And please mind the [code of conduct] for all interactions with the community.

## Versioning

Development of the app is currently still in alpha stage, and current versioning
is for internal use only. In the future, we are aiming to adopt [semantic
versioning] that is synchronized to the versioning of [TEStribute] and
[DRS-cli] in order to ensure that these apps will be compatible as long as both
their major and minor versions match.

## License

This project is covered by the [Apache License 2.0] also available [shipped
with this repository](LICENSE).

## Contact

Please contact the [project leader](mailto:alexander.kanitz@sib.swiss) for
inquiries, proposals, questions etc. that are not covered by the
[Contributing](#Contributing) section.

## Acknowledgments

The project is a collaborative effort under the umbrella of the [ELIXIR Cloud
and AAI] group. It was started during the [2019 Google Summer of Code] as part
of the [Global Alliance for Genomics and Health] [organization].


![logo banner]

[2019 Google Summer of Code]: <https://summerofcode.withgoogle.com/projects/#6613336345542656>
[Apache License 2.0]: <https://www.apache.org/licenses/LICENSE-2.0>
[code of conduct]:CODE_OF_CONDUCT.md
[Connexion]:https://github.com/zalando/connexion
[config]: mock_drs/config/app_config.yaml
[config specifications]: mock_drs/specs/schema.data_repository_service.config_update.openapi.yaml
[contributing guidelines]: CONTRIBUTING.md
[Data Repository Service]:https://github.com/ga4gh/data-repository-service-schemas
[DRS-cli]:https://github.com/elixir-europe/DRS-cli
[modified DRS specification]:mock_drs/specs/schema.data_repository_service.cd0186f.openapi.modified.yam
[extended DRS specification]:mock_drs/specs/schema.data_repository_service.cd0186f.openapi.modified.yam
[Global Alliance for Genomics and Health]: <https://www.ga4gh.org/>
[logo banner]:logos/logo-banner.svg
[organization]: <https://summerofcode.withgoogle.com/organizations/6643588285333504/>
[semantic versioning]:<https://semver.org/>
[TEStribute]:https://github.com/elixir-europe/TEStribute
