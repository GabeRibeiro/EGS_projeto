import nodemailer, {Transporter} from 'nodemailer';
import {NotificationDto} from "@/features/sendNotification/Notification.dto";
import {notifyUser} from "@/socketio";
import {logger} from "@/logger";
import {insertNotification} from "@/db";
import {NotificationModel} from "@/db/models/Notification.model";

const _emailFrom = "example@example.com";
const _emailSubject = "Price Update!";

let _transporter:Transporter = null;

async function _getTransporter() {
    if (_transporter) {
        return _transporter;
    }
    const testAccount = await nodemailer.createTestAccount();
    // create reusable transporter object using the default SMTP transport
    _transporter = nodemailer.createTransport({
        host: "smtp.ethereal.email",
        port: 587,
        secure: false, // true for 465, false for other ports
        auth: {
            user: testAccount.user, // generated ethereal user
            pass: testAccount.pass, // generated ethereal password
        },
    });
    return _transporter;
}

// todo email notification
export async function sendEmail(msgText:string, recipient:string) {
    const transporter = await _getTransporter();
    const info = await transporter.sendMail({
        from: _emailFrom,
        to: recipient,
        subject: _emailSubject,
        text: msgText
    });
    logger.info("Email Sent to: "+recipient);
}

// todo pnone text notification
export async  function sendText(msgText: string, recipient:number) {
    logger.info("Text Sent to: "+recipient);
    return;
}

export const persistNotification = async (notification:NotificationDto): Promise<NotificationModel> => {
        return await insertNotification(notification.uid, null);
}

export async function notifyQueue(notification:NotificationModel) {
    await notifyUser(notification.uid, notification);
}

