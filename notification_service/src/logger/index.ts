import * as winston from "winston";
import * as morgan from 'morgan';
import {RequestHandler} from "express";
import {DEBUG} from '@/const';

export const log = console.log;
export const warn = console.warn;

// winston format
const { combine, timestamp, printf } = winston.format;

// Define log format
// tslint:disable-next-line:no-shadowed-variable
const logFormat = printf(({ timestamp, level, message }) => `${timestamp} ${level}: ${message}`);

export const logger = winston.createLogger({
    format: combine(
        timestamp({
            format: 'YYYY-MM-DD HH:mm:ss',
        }),
        logFormat,
    ),
    exitOnError: false,
    level: DEBUG? 'debug':'info',
    transports: [
        new (winston.transports.Console)(),
        new (winston.transports.File)({ filename: 'app.log'})
    ]
})

const myStream = {
    write: (text: string) => {
        logger.info(text)
    }
}

export const expressLogMidlleware:RequestHandler = morgan('combined', { stream: myStream });

