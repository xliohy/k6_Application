import http from 'k6/http';
import { check } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

const DOMAIN = __ENV.DOMAIN;

export const options = {
  stages: [
    { duration: '30s', target: 300 },
    { duration: '2m', target: 3500 },
    { duration: '30s', target: 700 },
    { duration: '2m', target: 5000 },
  ],
};

export default function () {
  const url = `${DOMAIN}/v1/token`;
  const payload = JSON.stringify({
    length: randomIntBetween(256, 500),
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = http.post(url, payload, params);

  check(response, {
    'is status 201': (r) => r.status === 201,
  });
}
