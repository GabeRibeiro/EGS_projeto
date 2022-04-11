import {Router} from "express";

import {persistenceController} from "./persistence.controller";
import {authMiddleware, dtoValidationMiddleware} from "@/middlewares";
import {PaginationDto} from "@/features/persistentNotifications/pagination.dto";

export const persistenceRoute = Router();

persistenceRoute.get('/', authMiddleware, dtoValidationMiddleware(PaginationDto, 'query'), persistenceController);
