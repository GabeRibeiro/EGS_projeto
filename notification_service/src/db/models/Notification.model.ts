export class NotificationModel {
    uid: string;
    pid: number;
    txt: string;

    constructor(uid: string, pid: number, txt: string) {
        this.uid = uid;
        this.pid = pid;
        this.txt = txt;
    }
}