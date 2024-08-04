const PROXY_HOST = 'http://127.0.0.1:8000';

const PROXY_CONFIG = [
    {
        context: ['/api'],
        target: 'PROXY_HOST',
        secure: false
    }
];

module.exports = PROXY_CONFIG