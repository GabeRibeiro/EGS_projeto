import {RequestHandler} from "express";
import {RequestWithUser} from "@/interfaces/auth.interface";
import {getNotifications} from "@/db";


export const persistenceController: RequestHandler = async (req:RequestWithUser, res) => {
    const notifications = await getNotifications(req.user.uid);
    res.json(JSON.stringify(notifications));
}