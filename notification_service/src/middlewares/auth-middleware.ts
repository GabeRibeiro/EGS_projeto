import {RequestHandler} from 'express';
import {RequestWithUser, SocketWithUser} from "@/interfaces/auth.interface";
import HttpException from "@/exceptions/HTTPException.exception";
import {User} from "@/interfaces/user.interface";

/** todo
 * validates an auth token and returns a User (user.interface).
 * @param token token to be validated.
 */
const validateAuthToken = token => {
    if(!token) {
        return null;
    }
    return {uid: Number(token)} as User;
}

/**
 * Midlleware to authenticate users for calling a REST endpoint (express app).
 * If token isn't valid, calls next with a HttpException().
 * @param req
 * @param res
 * @param next
 */
export const authMiddleware: RequestHandler =  (req:RequestWithUser, res, next) => {
    const authHeader = req.header('Authorization');

    if(!authHeader){
        next(new HttpException(401, "Not Authorized!"));
    }

    // extract user data
    // check user auththorization w auth service
    const user= validateAuthToken(authHeader);

    if(!authHeader) {
        next(new HttpException(401, "Not Authorized!"));
    }

    req.user=user;
    next();
}

/**
 * Midlleware to authenticate SocketIO calls.
 * If token isn't valid, calls next with a HttpException().
 * @param socket Current socket connection.
 * @param next
 */
export const authMidllewareSIO = (socket:SocketWithUser,  next) => {
    const token = socket.handshake.auth.token;
    if (!token) {
        next(new HttpException(401, "Not Authorized!"));
    }

    // verify token
    const user = validateAuthToken(token);

    if(!user) {
        next(new HttpException(401, "Not Authorized!"));
    }

    socket.user = user;
    next();
}