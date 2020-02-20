# mock-DRS

[![Apache License](https://img.shields.io/badge/license-Apache%202.0-orange.svg?style=flat&color=important)](http://www.apache.org/licenses/LICENSE-2.0)

[Connexion]-based mockup service implementing parts of the GA4GH [Data Repository
Service] (DRS) API schema. The service was developed to implement and test
[TEStribute], a task distribution logic package for TES instances.

## Usage

Once deployed and started ([see below](#Deployment)), the service is available at:  
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

The client [DRS-cli] can be used to send requests to the service.

## Deployment

`mock-DRS` can be deployed via containers (preferred) or after manual
installation of all dependencies.

In both cases, the repository first needs to be cloned with:

```bash
git clone git@github.com:elixir-europe/mock-DRS.git
```

Afterwards traverse to the repository's root directory:

```bash
cd mock-DRS
```

### Containerized Deployment

> "Production-like" containerized deployment without HTTP server/load balancer
> etc.

#### Requirements (containerized deployment)

- [Git] (tested with version 2.17.1)
- [Docker] (tested with version 18.09.6)
- [docker-compose] (tested with version 1.24.0)

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

### Non-containerized deployment

> Deployment for local development without containers, HTTP server/load
> balancer etc.

#### Requirements (non-containerized deployment)

- [Git] (tested with version 2.17.1)
- [Python] (tested with versions 2.7.15+ & 3.6.8)
- [pip] (tested with version 19.1.1)
- [virtualenv] (tested with version 15.1.0)

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

> **IMPORTANT:** You will also need to replace host `mongo` with `localhost` in
> the `database` section of the [config] file.

## Implementation details

Note that only those parts of the service are implemented that are required for
developing, testing and debugging [TEStribute]. For all other endpoints only
stubs are implemented that return the most basic valid response (typically an
"empty" JSON object).

### Assumptions not warranted by DRS specifications

- As the current [DRS specifications] do not provide a means to identify
  identical objects across DRS instances (e.g., via a mandatory checksum),
  [TEStribute] assumes that DRS identifiers (property `id` of `Object` model)
  are globally unique across the network of DRS instances. While this assumption
  is not warranted by the specifications, it might perhaps be possible to
  enforce a common naming scheme at least within a given organization, until a
  more sustainable solution arises.

### The DRS Database

When starting the service, the DRS is automatically populated with a set of
objects from a [data objects] file. The identifiers of the objects that the
database is populated with are in turn specified in the [config] file.

#### Custom data objects

> **IMPORTANT:** When populating DRS instances for the use with [TEStribute]
> in the manner described here, you **must** ensure that all object identfiers
> are globally unique across the entire network of connected/used DRS services.
> See the section on [assumptions not warranted by DRS
> specifications](#assumptions-not-warranted-by-drs-specifications) for
> details.

The service can be configured to be started with different data objects by
first editing/amending the [data objects] file and then editing the
`database -> objects` section of the [config] file before starting the service.
Only objects specified in [data objects] are available to the DRS service at
startup, so make sure that any object that is added to the [config] file has a
corresponding entry in the [data objects] file.

Alternatively (and preferably), objects available to the DRS can be modified
in the running service via the `/update-db` endpoint, which is particularly
useful for setting up environments for various testing scenarios for
[TEStribute]. The endpoint is defined in a dedicated [OpenAPI] [specification]:

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
            $ref: '#/definitions/UpdateObject'
          required: true
      responses:
        200:
          description: "200 response"
          schema:
              $ref: '#/definitions/UpdatedDB'
      tags:
        - DataRepositoryService
      x-swagger-router-controller: ga4gh.drs.server
```

It relies on the following models:

```yaml
UpdatedDB:
  type: object
  properties:The service can be configured with different unit costs for CPU and memory
    objects:
      type: ausage, data transfer and storage. Default values for the corresponding
      items:
        type:parameters are listed in `task_info` section of the service's [config] and they
UpdateObject:can be edited by the user before starting the service.
  type: object
  properties:
    clear:
      type: boolean
    data_objects:
      type: array
      items:
        $ref: '#/definitions/Object'
```

The model `UpdateObject` in turn relies on the `Object` model of the [DRS
specifications], commit [`cd0186f`], a [snapshot] of which is also shipped with
this repository.

[DRS-cli] can be used to communicate with the `/update-db` endpoint.

> Note that while the `/update-db` endpoint can be accessed via the same root
> URI (and explored via the Swagger UI), it was not included in the [DRS
> specifications], but rather is added to it _on the fly_ when the service
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
[`cd0186f`]: <https://github.com/ga4gh/data-repository-service-schemas/blob/cd0186fa9b7763bdb15175e6615ff4a42c1b85c3/openapi/data_repository_service.swagger.yaml>
[code of conduct]: CODE_OF_CONDUCT.md
[config]: mock_drs/config/app_config.yaml
[Connexion]: <https://github.com/zalando/connexion>
[data objects]: mock_drs/database/data_objects.json
[Docker]: <https://docs.docker.com/install/>
[docker-compose]: <https://docs.docker.com/compose/install/>
[specification]: mock_drs/specs/schema.data_repository_service.update_db.openapi.yaml
[contributing guidelines]: CONTRIBUTING.md
[Data Repository Service]: <https://github.com/ga4gh/data-repository-service-schemas>
[DRS-cli]: <https://github.com/elixir-europe/DRS-cli>
[DRS specifications]: <https://github.com/ga4gh/data-repository-service-schemas>
[ELIXIR Cloud and AAI]: <https://elixir-europe.github.io/cloud/>
[snapshot]: mock_drs/specs/schema.data_repository_service.cd0186f.openapi.yaml
[Git]: <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>
[Global Alliance for Genomics and Health]: <https://www.ga4gh.org/>
[logo banner]: logos/logo-banner.svg
[OpenAPI]: <https://swagger.io/specification/>
[organization]: <https://summerofcode.withgoogle.com/organizations/6643588285333504/>
[pip]: <https://pip.pypa.io/en/stable/installing/>
[Python]: <https://www.python.org/downloads/>
[semantic versioning]: <https://semver.org/>
[TEStribute]: <https://github.com/elixir-europe/TEStribute>
[virtualenv]: <https://virtualenv.pypa.io/en/stable/installation/>
