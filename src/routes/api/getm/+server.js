import { error, json } from '@sveltejs/kit';
import mysql from 'mysql2/promise';

const dbHost = process.env.DB_HOST;
const dbUser = process.env.DB_USER;
const dbPassword = process.env.DB_PASSWORD;
const dbName = process.env.DB_NAME;

const connection = await mysql.createConnection({
    host: dbHost,
    user: dbUser,
    password: dbPassword,
    database: dbName,
});

async function getPostFromDatabase() {
    try {
        const [results, fields] = await connection.query(
            'SELECT * FROM `billing_info`
        );

        console.log(results); // results contains rows returned by server
        console.log(fields); // fields contains extra meta data about results, if available
        return results;
    } catch (err) {
        console.log(err);
    }
}

/** @type {import('./$types').RequestHandler} */
export async function GET({ url }) {
    const res = await getPostFromDatabase()

    console.log(res)

    return json(res);
}