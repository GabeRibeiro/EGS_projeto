# Notification Service
v0.3

This service provides the handling of generic notifications.

OpenApi description is available [here](./docs/api.yaml).

## Features
- Real time push notification support (with message queue support)
- Notification Persistence (with pagination support)
- Email Notification

### Push Notifications
Push notifications are implemented using the Socket.IO library, as such, integration with a push notification client is somewhat trivial.

In the folder [fe_sdk](./fe_sdk) there is an example of usage.

### Not yet implemented

### Not going to implement:
- Phone Text Notification: due to the need of having  a mobile number all services found charge some money for its usage, unlike email.

## Execution
This service can be run either by using the provided docker compose files or by building the source and execute it by hand, however that requires manual installation of its dependencies.

### Docker Compose
Both a dockerfile and a docker compose + postgres init sql files are provided and can be found in the [deploy](deploy) folder.

### Source

This service can be built and executed by using the provided npm scripts.

#### Dependencies:
The following dependecies have to be present in the system:
- NodeJS >= v16
- PostgresSQL server

To install all the other required dependencies automatically:

`$ npm ci`

Edit the .env files with the required values (template in .env.template).

To build and start server:

`$ npm run start`


## Todo:
- [x] Integration of auth service
- [x] Email notification
- [x] Notification Persistence Pagination
- [x] Docker image file
- [x] Docker compose file
- [ ] Improve documentation (ongoing)
- [ ] Improve logging (ongoing)
