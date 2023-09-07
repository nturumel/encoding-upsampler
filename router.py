from flask import Flask, request, jsonify
import torch
import csv
import os
import uuid
from threading import Thread, Lock
from queue import Queue

app = Flask(__name__)

# Load the model
model = torch.load("best_model.pth")
model.eval()

# Initialize queue and lock
job_queue = Queue()
lock = Lock()

# Dictionary to keep track of batch requests
batch_status = {}


def get_unit_vector(tensor):
    return tensor / torch.norm(tensor, dim=1, keepdim=True)


def process_queue():
    while True:
        job = job_queue.get()
        if job["type"] == "batch":
            process_batch_job(job)
        elif job["type"] == "realtime":
            process_realtime_job(job)
        job_queue.task_done()


def process_batch_job(job):
    batch_request_id = job["batch_request_id"]
    input_filepath = job["input_filepath"]
    output_filepath = job["output_filepath"]

    with open(input_filepath, "r") as infile, open(output_filepath, "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            embedding = torch.tensor([float(x) for x in row]).unsqueeze(0)
            upsampled_embedding = model(embedding).squeeze().detach().numpy()
            writer.writerow(upsampled_embedding)

            with lock:
                batch_status[batch_request_id]["num_records_processed"] += 1

    with lock:
        batch_status[batch_request_id]["status"] = "COMPLETED"


@app.route("/batch_request", methods=["POST"])
def batch_request():
    input_filepath = request.args.get("input_filepath")
    output_filepath = request.args.get("output_filepath")

    batch_request_id = str(uuid.uuid4())
    with lock:
        batch_status[batch_request_id] = {
            "status": "IN_PROGRESS",
            "num_records_processed": 0,
        }

    job = {
        "type": "batch",
        "batch_request_id": batch_request_id,
        "input_filepath": input_filepath,
        "output_filepath": output_filepath,
    }
    job_queue.put(job)

    return jsonify({"batch_request_id": batch_request_id})


@app.route("/batch_status", methods=["GET"])
def batch_status_request():
    batch_request_id = request.args.get("batch_request_id")
    with lock:
        if batch_request_id in batch_status:
            return jsonify(batch_status[batch_request_id])
        else:
            return jsonify({"status": "FAILED", "reason": "Invalid batch_request_id"})


@app.route("/realtime_request", methods=["POST"])
def realtime_request():
    input_embedding = request.json["input_embedding"]
    tensor_embedding = torch.tensor(input_embedding).unsqueeze(0)
    upsampled_embedding = model(tensor_embedding).squeeze().detach().numpy().tolist()

    return jsonify({"upsampled_embedding": upsampled_embedding})


if __name__ == "__main__":
    # Start queue processing thread
    worker = Thread(target=process_queue)
    worker.setDaemon(True)
    worker.start()

    app.run(debug=True)
