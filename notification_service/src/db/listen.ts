import createSubscriber from "pg-listen"
import {dbConfig} from "@/db/index";

const subscriber = createSubscriber(dbConfig);

subscriber.events.on("error", (error) => {
    console.error("Fatal database connection error:", error)
    process.exit(1)
})

process.on("exit", () => {
    subscriber.close();
})

export const initListenNotify = async () => {
    await subscriber.connect();
}

export const registerSub = async (uid: string, callback: (object) => void ) => {
    subscriber.notifications.on(uid, payload => {
        callback(payload);
    })
    await subscriber.listenTo(uid);
};

export const unlisten = async (uid: string) => {
    await subscriber.unlisten(uid);
}
// export const unregisterSub = async (uid: string, callback ) => {
//     subscriber.notifications.on(uid, payload => {
//         callback(payload);
//     })
//     await subscriber.listenTo(uid);
// };

export const emitNotify = async (uid: string, payload) => {
    await subscriber.notify(uid, payload);
}