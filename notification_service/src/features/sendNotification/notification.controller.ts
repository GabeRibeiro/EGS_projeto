import {RequestHandler} from "express";
import {NotificationDto} from "@/features/sendNotification/Notification.dto";
import {notifyQueue, persistNotification, sendEmail, sendText} from "@/features/sendNotification/notification.service";
import {NotificationModel} from "@/db/models/Notification.model";


export const notificationController: RequestHandler = async (req, res) => {
    const notification: NotificationDto = req.body;
    const options = notification.options;
    let pid =-1;

    if(options.email) {
        console.log("@notificationController: sending email");
        await sendEmail(notification.text, options.email);
    }

    if (options.phoneNumber) {
        console.log("@notificationController: sending text");
        await sendText(notification.text, options.phoneNumber);
    }

    if (options.persist) {
        console.log("@notificationController: notification persist");
        pid = (await persistNotification(notification)).pid;
    }

    const n = new NotificationModel(notification.uid, pid, notification.text)
    await notifyQueue(n);

    res.sendStatus(200)
}