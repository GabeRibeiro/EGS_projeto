import {Pool} from 'pg';
import {NotificationModel} from "@/db/models/Notification.model";
import {logger} from "@/logger";

const getPool = (() => {
    let _pool = null;
    return (() => {
        if(!_pool) {
            _pool = new Pool();
        }
        let connected = false;
        while(!connected) {
            testConnection().then(() => {
                logger.info('🟢 The database is connected.');
                connected = true;
            })
                .catch(error => {
                    logger.error(`🔴 Unable to connect to the database: ${error}.`);
                })
        }
        return _pool;
    });
})();

export const initDB = getPool;

export const pool = getPool();

export const testConnection = async () => {
    return await pool.query("SELECT NOW()");
}

export const getDormantNotifications = async (uid:string): Promise<NotificationModel[]> => {
    const result = await pool.query("Select * from notificationQueue where uid=$1", [uid]);
    return result.rows.map(row => new NotificationModel(row.uid, row.pid, row.msg)) as NotificationModel[];
}

export const deleteDormantNotifications = async (uid:string): Promise<boolean> => {
    try{
        await pool.query("delete FROM notificationQueue where uid= $1", [uid]);
        return true;
    } catch (e) {
        return false;
    }
}

export const insertDormantNotification = async (uid:string, text:string, pid?:number): Promise<boolean> => {
    try{
        if (pid) {
            await pool.query("insert into notificationQueue(uid, pid, msg) values ($1, $2, $3)", [uid, pid, text]);
        } else {
            await pool.query("insert into notificationQueue(uid, msg) values ($1, $2)", [uid, text]);
        }
        return true;
    } catch (e) {
        return false;
    }
}

export const insertDormantNotificationModel = async (n: NotificationModel): Promise<boolean> => {
    return insertDormantNotification(n.uid, n.txt, n.pid);
}

export const getNotifications = async (uid:string, nrPage?:number, resultsPerPage?:number): Promise<NotificationModel[]> => {
    let lastIdx = 0;

    try {
        lastIdx = (await pool.query("select id from notification where uid=$1 order by id desc limit 1;", [uid])).rows[0].id;
    } catch (e) {
        console.log("@getNotifications err: "+e)
    }

    try{
        const params:(string | number)[] = [uid];
        let wherePart ="";
        let limitPart = ""

        if(nrPage >= 1 && resultsPerPage >= 1) {
            wherePart = `and id <= $2`;  params.push(lastIdx-(nrPage-1)*resultsPerPage);
            limitPart = "limit $3";  params.push(resultsPerPage);
        }

        const query = `Select * from notification where uid=$1 ${wherePart} order by id desc ${limitPart}`;
        const result = await pool.query(query, params);
        return result.rows.map(r => new NotificationModel(r.uid, r.id, r.msg));
    } catch (e) {
        throw e;
    }
}

export const insertNotification = async (uid:string, text:string): Promise<NotificationModel> => {
    try{
        const res = await pool.query("insert into notification(uid, msg) values ($1, $2) RETURNING id", [uid, text]);
        return new NotificationModel(uid, res.rows[0].id, text);
    } catch (e) {
        return null;
    }
}
