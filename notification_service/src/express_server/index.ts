import * as express from 'express'
export const app = express();

// MIDDLEWARES

import * as cors from 'cors';

app.use(cors());
app.use(express.json());

import {expressLogMidlleware} from "@/logger";
app.use(expressLogMidlleware);

// ROUTES
import {router} from "./routes";
app.use(router);