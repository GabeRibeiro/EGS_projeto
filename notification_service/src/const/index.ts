console.log("Reading env...")

export const DEBUG = (process.env.DEBUG && process.env.DEBUG.valueOf() === "true".valueOf()) || false;
export const AUTH_DEBUG = (process.env.AUTH_DEBUG && process.env.AUTH_DEBUG.valueOf() === "true".valueOf()) || false;

if(DEBUG) {
    console.log("DEBUG active")
}

if(AUTH_DEBUG) {
    console.log("AUTH_DEBUG active")
}