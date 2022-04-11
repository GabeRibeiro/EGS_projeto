import {Router} from "express";

import {NotificationDto} from "@/features/sendNotification/Notification.dto";
import {notificationController} from "./notification.controller";
import {dtoValidationMiddleware} from "@/middlewares";

export const sendNotificationRoute = Router();

sendNotificationRoute.post('/', dtoValidationMiddleware(NotificationDto, "body"), notificationController);
