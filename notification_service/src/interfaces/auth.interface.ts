import {Request} from "express";
import {Socket} from "socket.io";
import {User} from './user.interface';

export interface RequestWithUser extends Request{
    user:User;
}

export class SocketWithUser extends Socket {
    user:User;
}