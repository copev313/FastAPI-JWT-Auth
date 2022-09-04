# FastAPI-JWT-Auth
 A FastAPI app that utilizes JWT authentication for protected routes. This project uses Deta Micro & Base for hosting the app, as well as a NoSQL database.


---------------
## Specs

 **Deta Version**: v1.3.3-beta

 - Creating a [new deta project](https://docs.deta.sh/docs/cli/commands/#deta-new).

 - [Deploy](https://docs.deta.sh/docs/cli/commands/#deta-deploy) local code & dependencies to the deta Micro server.

--------
## To Run

Execute the following command from the _fastapi_jwt_auth_ directory:

    uvicorn --host=0.0.0.0 --port 8000 --reload "main:app"

