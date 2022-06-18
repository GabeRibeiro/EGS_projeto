import {RequestHandler} from 'express';
import axios from 'axios';
import * as jwt from 'jsonwebtoken';
import {RequestWithUser, SocketWithUser} from "@/interfaces/auth.interface";
import HttpException from "@/exceptions/HTTPException.exception";
import {User} from "@/interfaces/user.interface";
import {logger} from "@/logger";
import {AUTH_DEBUG} from "@/const";

/**
 * validates an auth token and returns a User (user.interface).
 * @param token token to be validated.
 * (as per auth service definition, token has a jwt format but still needs to be verified with remote service)
 */
const validateAuthToken = async (token:string)  => {
    if(!token) {
        return null;
    }

    if(AUTH_DEBUG) {
        logger.debug("@validateAuthToken DEBUG MODE")
        return {uid: token} as User;
    }

    // check validity of the token with auth service
    let response = null;
    try {
        response = await axios({
            url:process.env.AUTHSERVICE_VERIFY_URL,
            method: "POST",
            headers: {
                [process.env.AUTHSERVICE_VERIFY_HEADER]: token.replace(/(\r\n|\n|\r)/gm, "")
            }
        })
    }
    catch (err) {
        return null
    }

    // As of api definition, token can only be considered valid if response code == 200
    if(!response || response.status !== 200){
        // token isn't valid, therefore there is nothing to be returned
        return null;
    }

    // get token data (jwt format)
    const tokenData = await jwt.decode(token);

    logger.debug("@validateAuthToken token ok")

    return {uid: tokenData._id} as User;
}

/**
 * Midlleware to authenticate users for calling a REST endpoint (express app).
 * If token isn't valid, calls next with a HttpException().
 * @param req
 * @param res
 * @param next
 */
export const authMiddleware: RequestHandler =  async (req:RequestWithUser, res, next) => {
    const authHeader = req.header('Authorization');

    if(!authHeader){
        next(new HttpException(401, "Not Authorized!"));
    }

    // extract user data
    // check user authorization w auth service
    const user = await validateAuthToken(authHeader);

    if(!authHeader) {
        next(new HttpException(401, "Not Authorized!"));
    }

    req.user=user;
    next();
}

/**
 * Middleware to authenticate SocketIO calls.
 * If token isn't valid, calls next with a HttpException().
 * @param socket Current socket connection.
 * @param next
 */
export const authMidllewareSIO = async (socket:SocketWithUser,  next) => {
    const token = socket.handshake.auth.token;
    if (!token) {
        next(new HttpException(401, "Not Authorized!"));
    }

    // verify token
    const user = await validateAuthToken(token);

    if(!user) {
        return next(new HttpException(401, "Not Authorized!"));
    }

    socket.user = user;
    next();
}