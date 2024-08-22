from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import asyncio
from pydantic import BaseModel
import os
import re

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class DomainInput(BaseModel):
    domain: str

class DomainAndEndpointInput(BaseModel):
    domain_and_endpoint: str

@app.post("/run-k6-scenario1/")
async def run_k6(input_data: DomainInput):
    domain = input_data.domain
    script_path = "/root/scenario/scenario1.js" 

    env = os.environ.copy()
    env["DOMAIN"] = domain

    try:
        k6_process = await asyncio.create_subprocess_exec(
            "k6", "run", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        stdout, stderr = await k6_process.communicate()

        if k6_process.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr.decode())

        metrics = extract_metrics(stdout.decode())

        return {
            "status": "success",
            "metrics": metrics,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run-k6-scenario2/")
async def run_k6_scenario2(input_data: DomainAndEndpointInput):
    domain = input_data.domain_and_endpoint
    script_path = "/root/scenario/scenario2.js"  

    env = os.environ.copy()
    env["DOMAIN"] = domain

    try:
        k6_process = await asyncio.create_subprocess_exec(
            "k6", "run", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        stdout, stderr = await k6_process.communicate()

        if k6_process.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr.decode())

        metrics = extract_metrics(stdout.decode())

        return {
            "status": "success",
            "metrics": metrics,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run-k6-scenario3/")
async def run_k6_scenario3(input_data: DomainAndEndpointInput):
    domain_and_endpoint = input_data.domain_and_endpoint
    script_path = "/root/scenario/scenario3.js"  

    env = os.environ.copy()
    env["DOMAIN"] = domain_and_endpoint

    try:
        k6_process = await asyncio.create_subprocess_exec(
            "k6", "run", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        stdout, stderr = await k6_process.communicate()

        if k6_process.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr.decode())

        metrics = extract_metrics(stdout.decode())

        return {
            "status": "success",
            "metrics": metrics,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop-k6/")
async def stop_k6():
    try:
        process = await asyncio.create_subprocess_exec(
            "pkill", "-f", "k6",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        metrics_1 = fetch_metrics("/root/scenario/scenario1.js")
        metrics_2 = fetch_metrics("/root/scenario/scenario2.js")
        metrics_3 = fetch_metrics("/root/scenario/scenario3.js")

        return {"status": "success", "message": "K6 processes stopped", "metrics": {"metrics_1": metrics_1, "metrics_2": metrics_2, "metrics_3": metrics_3}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_metrics(script_path):
    try:
        process = subprocess.run(["k6", "run", script_path], capture_output=True, text=True)
        return extract_metrics(process.stdout)
    except Exception as e:
        return {"error": str(e)}

def extract_metrics(output):
    lines = output.splitlines()
    metrics = {}

    for line in lines:
        if "checks" in line:
            metrics["checks"] = extract_value(line)
        elif "data_received" in line:
            metrics["data_received"] = extract_value(line)
        elif "data_sent" in line:
            metrics["data_sent"] = extract_value(line)
        elif "http_req_blocked" in line:
            metrics["http_req_blocked"] = extract_value(line)
        elif "http_req_connecting" in line:
            metrics["http_req_connecting"] = extract_value(line)
        elif "http_req_duration" in line:
            metrics["http_req_duration"] = extract_value(line)
        elif "http_req_failed" in line:
            metrics["http_req_failed"] = extract_value(line)
        elif "http_req_receiving" in line:
            metrics["http_req_receiving"] = extract_value(line)
        elif "http_req_sending" in line:
            metrics["http_req_sending"] = extract_value(line)
        elif "http_req_tls_handshaking" in line:
            metrics["http_req_tls_handshaking"] = extract_value(line)
        elif "http_req_waiting" in line:
            metrics["http_req_waiting"] = extract_value(line)
        elif "http_reqs" in line:
            metrics["http_reqs"] = extract_value(line)
        elif "iteration_duration" in line:
            metrics["iteration_duration"] = extract_value(line)
        elif "iterations" in line:
            metrics["iterations"] = extract_value(line)
        elif "vus" in line:
            metrics["vus"] = extract_value(line)
        elif "vus_max" in line:
            metrics["vus_max"] = extract_value(line)

    return metrics


def extract_value(line):
    match = re.search(r':\s*(.*)', line)
    return match.group(1) if match else "N/A"
