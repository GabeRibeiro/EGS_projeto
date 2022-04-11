import {RequestHandler} from "express";

export const reqMiddleware= (part): RequestHandler => (req, res, next) => {
    console.log("Req Middleware:")
    console.log(req[part]);
    next()
}