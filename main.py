import datetime
import math
import random
import uuid
import argparse
import os
from pathlib import Path
import sys
import time
import concurrent.futures
import traceback

from generator import (
    generateAmount,
    generateDatetime,
    generateFileName,
    generateParty,
    generatePartyPair,
)
from writer import writeGraph

parties = []
transactions = []


def main():
    root_path = Path.cwd()

    my_parser = argparse.ArgumentParser(description="Generate Mock Transactions Data")
    my_parser.add_argument(
        "-o", "--output", help="the output path for the files", required=True
    )
    my_parser.add_argument(
        "-tc",
        "--transaction-count",
        help="the number of transactions to generate",
        required=True,
    )
    my_parser.add_argument(
        "-pc",
        "--parties-count",
        help="the number of parties to generate"
        "default is 10%% of transaction count",
        required=False,
    )
    my_parser.add_argument(
        "-mdb",
        "--max-days-before",
        help="the number of days over which transactions will be distributed (default is 3)",
        required=False,
        type=int,
        default=3,
    )
    my_parser.add_argument(
        "-thc",
        "--thread-count",
        help="the number of threads to use for writing the files (default is 20)",
        required=False,
        type=int,
        default=20,
    )
    my_parser.add_argument(
        "-fc",
        "--files-count",
        help="the number of files over which to distribute the transactions",
        required=True,
    )
    my_parser.add_argument(
        "-sp",
        "--suspicious-percentage",
        help="the percentage of suspicious transactions (default is 0.0001 = 0.01%%)",
        required=False,
        type=float,
        default=0.001,  # 0.1%
    )
    args = my_parser.parse_args()

    invoke_command(
        args.output,
        args.transaction_count,
        args.parties_count,
        args.max_days_before,
        args.thread_count,
        args.suspicious_percentage,
        args.files_count,
    )


def invoke_command(
    output_path,
    transaction_count,
    parties_count,
    max_days_before,
    thread_count,
    suspicious_percentage,
    number_of_files,
):
    print(f"The output path is \"{output_path}\"")
    if not os.path.isdir(output_path):
        print("The specified path does not exist: " + str(output_path))
        sys.exit()

    fileFormat = "nt"
    fileExtension = "nt"

    rows = int(transaction_count)
    if parties_count:
        partyCount = int(parties_count)
    else:
        partyCount = int(transaction_count) // 10
    batch_size = int(rows / int(number_of_files))

    now = datetime.datetime.utcnow()
    print("Generating: " + str(rows) + " Transactions.")
    print("Estimated batch size:" + str(batch_size))
    print("Start process. " + str(datetime.datetime.now()))
    start = time.time()

    maxDaysBefore = max_days_before
    print("Generating Parties")
    generate_parties(partyCount)
    print("Generating Transactions")
    generate_transactions(rows, now, maxDaysBefore)
    print("Generating suspicious Parties")
    generate_suspicious_parties(int(partyCount * suspicious_percentage))
    generate_files(batch_size, output_path, fileExtension, fileFormat, thread_count)
    print("Finished. " + str(datetime.datetime.now()))
    end = time.time()
    print("Total execution time: " + str(end - start) + " Seconds")
    print("Total execution time: " + str((end - start) / 60) + " Minutes")


def generate_parties(partyCount):
    # Generate parties
    for i in range(partyCount):
        internal = random.choice(["Y", "N"])
        party = {
            **generateParty(),
            "internal": internal,
            "isSuspicious": "N",
            "exited": random.choices(
                ["N", "Y" if internal == "N" else "N"], weights=[199, 1]
            )[0]
        }
        parties.append(party)


def generate_transactions(rows, now, maxDaysBefore):
    # Generate transactions
    for i in range(rows):
        partyPair = generatePartyPair(parties)

        transactions.append(
            {
                "id": uuid.uuid4().hex,
                "amount": generateAmount(),
                "date": generateDatetime(now, maxDaysBefore).isoformat(),
                "originator": partyPair[0],
                "beneficiary": partyPair[1],
            }
        )


def generate_suspicious_parties(rows):
    print("Updating {0} suspicious parties".format(rows))
    for i in range(rows):
        update_party = True
        while update_party:
            party = random.choice(parties)
            if party["isSuspicious"] == "N":
                party["isSuspicious"] = "Y"
                update_party = False

def generate_files(batch_size, outputPathCore, fileExtension, fileFormat, thread_count):
    print("Writing files to : " + str(outputPathCore))
    with concurrent.futures.ProcessPoolExecutor(max_workers=thread_count) as executor:
        for batchIndex in range(math.ceil(len(parties) / batch_size)):
            batchStart = batchIndex * batch_size
            batchEnd = batchStart + batch_size
            partyBatch = parties[batchStart:batchEnd]
            outputPath = generateFileName(
                str(outputPathCore), "parties", batchIndex, fileExtension
            )
            executor.submit(
                write_files_multi_threaded,
                "Thread #{0}".format(batchIndex),
                outputPath,
                fileFormat,
                partyBatch,
                [],
            )

    with concurrent.futures.ProcessPoolExecutor(max_workers=thread_count) as executor:
        for batchIndex in range(math.ceil(len(transactions) / batch_size)):
            batchStart = batchIndex * batch_size
            batchEnd = batchStart + batch_size
            transactionBatch = transactions[batchStart:batchEnd]
            outputPath = generateFileName(
                str(outputPathCore), "transactions", batchIndex, fileExtension
            )
            executor.submit(
                write_files_multi_threaded,
                "Thread #{0}".format(batchIndex),
                outputPath,
                fileFormat,
                [],
                transactionBatch,
            )


def write_files_multi_threaded(
    threadName, outputPath, fileFormat, partyBatch, transactionBatch
):
    try:
        print("thread {0} is working on file:".format(threadName))
        print(outputPath)
        writeGraph(str(outputPath), fileFormat, partyBatch, transactionBatch)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()
