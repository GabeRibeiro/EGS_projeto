import {RequestHandler} from 'express';
import {RequestWithUser, SocketWithUser} from "@/interfaces/auth.interface";
import HttpException from "@/exceptions/HTTPException.exception";

// todo: auth middleware
export const authMiddleware: RequestHandler =  (req:RequestWithUser, res, next) => {
    const authHeader = req.header('Authorization');
    if (authHeader) {
        // extract user data
        // check user auththorization w auth service
        req.user={uid: Number(authHeader)};
        next();
    } else {
        next(new HttpException(401, "Not Authorized!"));
    }
}

// todo: auth middleware SIO
export const authMidllewareSIO = (socket:SocketWithUser,  next) => {
    const token = socket.handshake.auth.token;
    if (token) {
        // verify token
        socket.user = {uid:token};
        next();
    } else {
        next(new HttpException(401, "Not Authorized!"));
    }
}