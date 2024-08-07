// src/routes/api/upload.js
import { json } from '@sveltejs/kit';

export async function OPTIONS() {
    return new Response(null, {
        headers: {
            'Access-Control-Allow-Origin': 'https://pesbit.ru',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    });
}

export async function POST({ request }) {
    const data = await request.formData();
    const file = data.get('file');

    if (!file) {
        return json({ error: 'No file uploaded' }, { status: 400 });
    }

    const response = await fetch('http://pyback:5000/upload', {
        method: 'POST',
        body: data,
        headers: {
            'Access-Control-Allow-Origin': 'https://pesbit.ru',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    });

    const result = await response.json();

    if (!response.ok) {
        return json(result, { status: response.status });
    }

    return json(result, {
        headers: {
            'Access-Control-Allow-Origin': 'https://pesbit.ru/',
        }
    });
}
