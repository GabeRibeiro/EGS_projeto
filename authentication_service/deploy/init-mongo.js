db.createUser(
    {
        user: "root",

        pwd: "egs4bodas",

        roles: [
            {
                role: "readWrite",
                db: "db"
            }
        ]
    }
);
db.createCollection("users");