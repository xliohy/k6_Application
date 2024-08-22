import http from 'k6/http';
import { check, sleep } from 'k6';

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime())).toISOString().split('T')[0];
}

function randomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function randomFirstName() {
    const names = [
        'John', 'Jane', 'Alice', 'Bob', 'Mike', 'Emily', 'Chris', 'Jessica', 'Matthew', 'Sarah',
        'Andrew', 'Amanda', 'David', 'Laura', 'James', 'Linda', 'Daniel', 'Sophia', 'Michael', 'Isabella',
        'Jacob', 'Mia', 'Ethan', 'Olivia', 'Alexander', 'Ava', 'William', 'Charlotte', 'Noah', 'Amelia',
        'Liam', 'Emma', 'Noah', 'Olivia', 'Aiden', 'Isabella', 'Jackson', 'Sophia', 'Caden', 'Avery'
    ];
    return randomElement(names);
}

function randomLastName() {
    const surnames = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
        'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
        'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
        'Young', 'Walker', 'King', 'Wright', 'Scott', 'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson'
    ];
    return randomElement(surnames);
}

function randomGender() {
    const genders = ['M', 'F'];
    return randomElement(genders);
}

const DOMAIN = __ENV.DOMAIN;

export const options = {
  stages: [
    { duration: '30s', target: 300 },
    { duration: '2m', target: 2000 },
    { duration: '30s', target: 700 },
    { duration: '2m', target: 3500 },
  ],
};

export default function () {
    const emp_no = randomInt(100000, 999999);  // 100000부터 999999까지의 랜덤 emp_no
    const birth_date = randomDate(new Date(1950, 0, 1), new Date(2005, 11, 31));  // 1950부터 2005년까지의 랜덤 출생일
    const first_name = randomFirstName();
    const last_name = randomLastName();
    const gender = randomGender();
    const hire_date = randomDate(new Date(1980, 0, 1), new Date(2023, 11, 31));  // 1980부터 2023년까지의 랜덤 고용일

    const payload = JSON.stringify({
        emp_no: emp_no,
        birth_date: birth_date,
        first_name: first_name,
        last_name: last_name,
        gender: gender,
        hire_date: hire_date
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const url = `${DOMAIN}/v1/employee`;

    const res = http.post(url, payload, params);

    check(res, {
        'status was 200': (r) => r.status === 200,
    });

    sleep(1);
}
