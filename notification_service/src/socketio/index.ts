import {SocketWithUser} from "@/interfaces/auth.interface";
import * as logger from "@/logger";
import * as db from '@/db';
import {NotificationModel} from "@/db/models/Notification.model";

const ioSocketMap = new Map<number, SocketWithUser>();

export const socketHandler = async (socket:SocketWithUser) => {
    const uid = socket.user.uid;
    logger.log('User connected: '+uid);
    socket.on('disconnect',  () => {
        ioSocketMap.delete(uid);
        logger.log('User disconnected: '+uid);
    });
    // register socket with a user
    ioSocketMap.set(uid, socket);
    // look for dormant notification
    const notifications = await db.getDormantNotifications(uid);
    for(const n of notifications) {
        console.log('n: '+n)
        socket.emit(SocketEvents.NewNotification, JSON.stringify(n));
    }
    await db.deleteDormantNotifications(uid);
}

export const getUserSocket = (uid: number) => {
    return ioSocketMap.get(uid);
}

export const isUserConnected = (uid: number) => {
    return ioSocketMap.get(uid) !== undefined;
}

export const notifyUser = async (uid:number, n:NotificationModel) => {
    const socket = ioSocketMap.get(uid);
    if (socket) {
        socket.emit(SocketEvents.NewNotification, n);
        return true;
    } else {
        await db.insertDormantNotificationModel(n);
        return false;
    }
}

