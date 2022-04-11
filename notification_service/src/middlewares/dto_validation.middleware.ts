import {RequestHandler} from "express";
import {plainToInstance} from 'class-transformer';
import {validate, ValidationError} from 'class-validator';
import HttpException from "../exceptions/HTTPException.exception";
import {DTO} from "@/interfaces/DTO";


export const dtoValidationMiddleware = (dto: DTO | any, inreq: string | 'body' | 'query' | 'params' = 'body', skipMissingProperties = false): RequestHandler => {
    return (req, _, next) => {
        validate(plainToInstance(dto, req[inreq]), {skipMissingProperties})
            .then((errors: ValidationError[]) => {
                if (errors.length > 0) {
                    const message = errors.map((error: ValidationError) => Object.values(error.constraints as { [type: string]: string })).join(', ');
                    next(new HttpException(400, message));
                } else {
                    next();
                }
            })
    }
}