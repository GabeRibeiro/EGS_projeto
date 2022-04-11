import * as dotenv from 'dotenv' // load .env
dotenv.config();

import {app} from '@/express_server';
import {createServer} from "http";
import {Server as ServerSIO} from "socket.io";
import {authMidllewareSIO} from "@/middlewares";
import {socketHandler} from "@/socketio";
import {testConnection} from "@/db";

import {logger} from '@/logger';

const httpServer = createServer(app);

const io = new ServerSIO(httpServer, {
    cors: {
        origin: '*',
        methods: ["GET", "POST"]
    }
});

// handle websocket connection auth
io.use(authMidllewareSIO);
io.on("connection", socketHandler);

// start the Express server
const port = process.env.SERVER_PORT; // default port to listen
httpServer.listen( port, () => {
    console.log( `server started at http://localhost:${ port }` );

    testConnection().then(() => {
        logger.info('🟢 The database is connected.');
    })
    .catch(error => {
        logger.error(`🔴 Unable to connect to the database: ${error}.`);
    })
} );


