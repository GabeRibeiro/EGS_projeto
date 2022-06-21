import {SocketWithUser} from "@/interfaces/auth.interface";
import {logger} from "@/logger";
import * as db from '@/db';
import {NotificationModel} from "@/db/models/Notification.model";
import {registerSub, unlisten} from "@/db/listen";

const ioSocketMap = new Map<string, SocketWithUser>();

export const socketHandler = async (socket:SocketWithUser) => {

    const uid = socket.user.uid;

    if(!uid) {
        return
    }

    logger.debug('@socketHandler User connected: '+uid);
    socket.on('disconnect',  () => {
        ioSocketMap.delete(uid);
        unlisten(uid);
        logger.debug('@socketHandler User disconnected: '+uid);
    });
    // register socket with a user
    ioSocketMap.set(uid, socket);
    // look for dormant notification
    const notificationsDB = await db.getDormantNotificationTransction(uid);
    for(const n of notificationsDB) {
        socket.emit(SocketEvents.NewNotification, JSON.stringify(n));
    }

    registerSub(uid, async (payload) => {
        // tslint:disable-next-line:no-shadowed-variable
        const notificationsDB = await db.getDormantNotificationTransction(uid);
        for(const n of notificationsDB) {
            console.log('@socketHandler n: '+n.txt )
            socket.emit(SocketEvents.NewNotification, JSON.stringify(n));
        }
    });
}

export const getUserSocket = (uid: string) => {
    return ioSocketMap.get(uid);
}

export const isUserConnected = (uid: string) => {
    return ioSocketMap.get(uid) !== undefined;
}

export const notifyUser = async (uid:string, n:NotificationModel) => {
    const socket = ioSocketMap.get(uid);



    if (socket) {
        logger.debug('@notifyUser: notification pushed; uid: '+uid);
        socket.emit(SocketEvents.NewNotification, n);
        return true;
    } else {
        logger.debug('@notifyUser: notification sent no dormant queue; uid: '+uid);
        await db.insertDormantNotificationModel(n);
        return false;
    }
}

