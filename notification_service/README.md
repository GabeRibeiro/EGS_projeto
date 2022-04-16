# Notification Service
v0.3

This service provides the handling of generic notifications.

OpenApi description is available [here](./docs/api.yaml).

## Features
- Real time push notification support (with message queue support)
- Notification Persistence

### Push Notifications
Push notifications are implemented using the Socket.IO library, as such, integration with a push notification client is relatively trivial.

In the folder [fe_sdk](./fe_sdk) theres is an example of usage.

### Not yet implemented
- Email Notification
- Phone Text Notification
- Notification Persistence Pagination


## Execution
At the moment this service can only be built and executed by using npm scripts.

### Dependencies:
The following dependecies have to be present in the system:
- NodeJS >= v16
- PostgresSQL server

To install all the other required dependencies automatically:

`$ npm ci`

Edit the .env files with the required values (template in .env.template).

To build and start server:

`$ npm run start`



## Todo:
- [ ] Integration of auth service
- [x] Email notification
- [ ] Phone Text notification
- [x] Notification Persistence Pagination
- [ ] Docker image and docker compose files
- [ ] Improve documentation
- [ ] Improve logging
