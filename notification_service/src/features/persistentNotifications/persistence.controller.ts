import {RequestHandler} from "express";
import {RequestWithUser} from "@/interfaces/auth.interface";
import {getNotifications} from "@/db";
import {PaginationDto} from "@/features/persistentNotifications/pagination.dto";
import HttpException from "@/exceptions/HTTPException.exception";

export const persistenceController: RequestHandler = async (req:RequestWithUser, res, next) => {
    const pagination: PaginationDto = {nrPage: Number(req.query.nrPage), resultsPerPage: Number(req.query.resultsPerPage)};
    let notifications = null;
    try {
        if (pagination.nrPage) {
            notifications = await getNotifications(req.user.uid, pagination.nrPage, pagination.resultsPerPage);

        } else {
            notifications = await getNotifications(req.user.uid);
        }
        res.json(JSON.stringify(notifications));
    } catch (err) {
        next(new HttpException(500, err))
    }
}