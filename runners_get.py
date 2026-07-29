import csv
import json
import os
import time
from pathlib import Path

import requests
import urllib3


# ============================================================
# CONFIGURATION
# ============================================================

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG = os.getenv("GITHUB_ORG", "zilvertonz")

BASE_URL = "https://api.github.com"

OUTPUT_DIR = Path("runner_inventory")
OUTPUT_DIR.mkdir(exist_ok=True)

VERIFY_SSL = False
REQUEST_TIMEOUT = 60

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
}

if not VERIFY_SSL:
    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )


# ============================================================
# API REQUEST
# ============================================================

def github_request(
    endpoint: str,
    params: dict | None = None,
):

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=REQUEST_TIMEOUT,
        verify=VERIFY_SSL,
    )

    if response.status_code in (403, 404):

        print(
            f"WARNING: {response.status_code} "
            f"for {endpoint}"
        )

        try:
            print(
                response.json().get(
                    "message"
                )
            )
        except Exception:
            print(response.text)

    response.raise_for_status()

    return response


# ============================================================
# RUNNERS
# ============================================================

def get_organization_runners():

    endpoint = (
        f"/orgs/{ORG}/actions/runners"
    )

    runners = []

    page = 1

    while True:

        print(
            f"GET {endpoint} "
            f"[page {page}]"
        )

        response = github_request(
            endpoint,
            {
                "per_page": 100,
                "page": page,
            },
        )

        data = response.json()

        page_runners = data.get(
            "runners",
            [],
        )

        runners.extend(
            page_runners
        )

        if len(page_runners) < 100:
            break

        page += 1

        time.sleep(0.1)

    return runners


# ============================================================
# FORMAT RESULTS
# ============================================================

def build_runner_inventory(
    runners: list,
):

    inventory = []

    for runner in runners:

        labels = runner.get(
            "labels",
            [],
        )

        inventory.append({
            "organization":
                ORG,

            "runner_id":
                runner.get("id"),

            "name":
                runner.get("name"),

            "os":
                runner.get("os"),

            "status":
                runner.get("status"),

            "busy":
                runner.get("busy"),

            "ephemeral":
                runner.get("ephemeral"),

            "version":
                runner.get("version"),

            "labels":
                ", ".join(
                    label.get(
                        "name",
                        ""
                    )
                    for label
                    in labels
                ),
        })

    return inventory


# ============================================================
# EXPORT CSV
# ============================================================

def export_csv(
    filename: str,
    records: list,
):

    if not records:

        print(
            "No runners found."
        )

        return

    path = (
        OUTPUT_DIR
        / filename
    )

    fields = [
        "organization",
        "runner_id",
        "name",
        "os",
        "status",
        "busy",
        "ephemeral",
        "version",
        "labels",
    ]

    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            records
        )

    print(
        f"Created: {path}"
    )


# ============================================================
# EXPORT JSON
# ============================================================

def export_json(
    filename: str,
    data,
):

    path = (
        OUTPUT_DIR
        / filename
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Created: {path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n================================"
    )

    print(
        "GitHub Organization Runner Inventory"
    )

    print(
        f"Organization: {ORG}"
    )

    print(
        "================================"
    )

    runners = (
        get_organization_runners()
    )

    inventory = (
        build_runner_inventory(
            runners
        )
    )

    export_csv(
        "organization_runners.csv",
        inventory,
    )

    export_json(
        "organization_runners.json",
        inventory,
    )

    online = sum(
        1
        for runner
        in inventory
        if runner["status"]
        == "online"
    )

    offline = sum(
        1
        for runner
        in inventory
        if runner["status"]
        == "offline"
    )

    busy = sum(
        1
        for runner
        in inventory
        if runner["busy"]
    )

    print()
    print(
        "================================"
    )

    print(
        "Runner Inventory Complete"
    )

    print(
        "================================"
    )

    print(
        f"Total runners: "
        f"{len(inventory)}"
    )

    print(
        f"Online: {online}"
    )

    print(
        f"Offline: {offline}"
    )

    print(
        f"Busy: {busy}"
    )


if __name__ == "__main__":
    main()