import {Router} from 'express'

export const router = Router();

import {sendNotificationRoute} from "features/sendNotification";
import {persistenceRoute} from "@/features/persistentNotifications";
router.use("/notification", sendNotificationRoute);
router.use('/notifications', persistenceRoute)