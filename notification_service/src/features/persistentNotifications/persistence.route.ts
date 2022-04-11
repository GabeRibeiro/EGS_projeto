import {Router} from "express";

import {persistenceController} from "./persistence.controller";
import {authMiddleware} from "@/middlewares";

export const persistenceRoute = Router();

persistenceRoute.get('/', authMiddleware, persistenceController);
