# Music Store

This repository contains a Python-based backend for a custom music store 
application. It leverages a MongoDB database to efficiently store and manage 
music-related data. Additionally, Docker and Docker Compose are employed to 
orchestrate two separate containers—one for the API and another for the MongoDB 
database—providing a seamless and scalable development environment


## Features

- **API Structure:** The project is organized to facilitate the addition of new features and APIs as the application evolves.
- **Modular Design:** The codebase is modular, making it easy to manage and expand upon.
- **MongoDB Integration:** MongoDB is used as the primary data store, offering flexibility and scalability for storing music-related information.
- **Dockerized Environment:** Docker and Docker Compose simplify the setup and deployment of the development environment.

## Getting Started:

1. Clone this repository to your local machine.
2. Ensure you have Docker and Docker Compose installed.
3. Run `docker-compose up` to start the containers.


## API Endpoints:

- `POST /auth/login`: API endpoints for managing songs.
- `GET /auth`: Get user email from token.
- `GET /cart`: Get user cart items.
- `POST /cart/items`: create cart and add cart items.
- `DELETE /cart/items/:item_id`: delete item from user cart.
- `DELETE /cart`: delete user cart.
- `PATCH /cart/items`: add cart items to user cart.
- `GET /catalog`: get all items in catalog.
- `POST /catalog`: create items for catalog.
- (Add more endpoints as needed)

## Usage:

This example backend provides a solid foundation for building your custom music 
store API. Feel free to use it as a starting point, adding your own features and
endpoints as required.

## Contributing:

We welcome contributions!

## License:

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
