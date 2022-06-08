import * as nodemailer from 'nodemailer';
import {NotificationDto} from "@/features/sendNotification/Notification.dto";
import {notifyUser} from "@/socketio";
import {logger} from "@/logger";
import {insertNotification} from "@/db";
import {NotificationModel} from "@/db/models/Notification.model";

const _emailSubject = "Price Update!";

let _transporter:nodemailer.Transporter = null;

async function _getTransporter() {
    if (_transporter) {
        return _transporter;
    }
    // const testAccount = await nodemailer.createTestAccount();
    // create reusable transporter object using the default SMTP transport
    _transporter = nodemailer.createTransport( {
        service:process.env.MAILSERVICE,
        auth: {
            user: process.env.MAILACCOUNT,
            pass: process.env.MAILPASSWD
        }
    });
    return _transporter;
}

export async function sendEmail(msgText:string, recipient:string) {
    try {
        const transporter = await _getTransporter();

        const info = await transporter.sendMail({
            from: process.env.MAILACCOUNT,
            to: recipient,
            subject: _emailSubject,
            text: msgText
        });
        logger.info("Email Sent to: "+recipient);
    } catch (e) {
        logger.error("Email not sent: "+recipient);
        logger.error(e.message);
    }
}

// todo pnone text notification
// not going to be implemented due to the cost, theres no free service
export async  function sendText(msgText: string, recipient:number) {
    logger.info("Text Sent to: "+recipient);
    return;
}

export const persistNotification = async (notification:NotificationDto): Promise<NotificationModel> => {
        return await insertNotification(notification.uid, notification.text);
}

export async function notifyQueue(notification:NotificationModel) {
    await notifyUser(notification.uid, notification);
}

