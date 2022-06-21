import * as dotenv from 'dotenv' // load .env
dotenv.config();

import {app} from '@/express_server';
import {createServer} from "http";
import {Server as ServerSIO} from "socket.io";
import {authMidllewareSIO} from "@/middlewares";
import {socketHandler} from "@/socketio";
import {initDB} from "@/db";

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
    logger.info( `server started at http://localhost:${ port }` );
    initDB();
} );


