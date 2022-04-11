export class NotificationModel {
    uid: number;
    pid: number;
    txt: string;

    constructor(uid: number, pid: number, txt: string) {
        this.uid = uid;
        this.pid = pid;
        this.txt = txt;
    }
}