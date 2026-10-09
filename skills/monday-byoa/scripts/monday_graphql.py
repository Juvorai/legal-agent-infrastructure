#!/usr/bin/env python3
"""Monday.com GraphQL client for a BYOA external agent.

Reads MONDAY_AGENT_API_TOKEN from the environment. Always sends API-Version: dev.
Never prints the token.
"""
import argparse
import json
import os
import sys
import urllib.request

API_URL = "https://api.monday.com/v2"


def get_token():
    token = os.environ.get("MONDAY_AGENT_API_TOKEN")
    if not token:
        sys.exit("MONDAY_AGENT_API_TOKEN is not set. Bind it as a secret on this agent.")
    return token


def monday_api(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": get_token(),
            "API-Version": "dev",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as res:
        data = json.loads(res.read().decode())
    if "errors" in data:
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data.get("data", data)


def cmd_me(_):
    print(json.dumps(monday_api("{ me { id name kind email account { id } } }"), indent=2))


def cmd_get_item(args):
    q = """
    query ($ids: [ID!]!) {
      items(ids: $ids) {
        id
        name
        board { id name }
        group { id title }
        column_values { id title text type }
        updates(limit: 10) { id text_body created_at creator { id name } }
      }
    }"""
    print(json.dumps(monday_api(q, {"ids": [str(args.item_id)]}), indent=2))


def cmd_create_update(args):
    q = """
    mutation ($itemId: ID!, $body: String!, $parentId: ID) {
      create_update(item_id: $itemId, body: $body, parent_id: $parentId) { id text_body }
    }"""
    variables = {"itemId": str(args.item_id), "body": args.body}
    if args.parent_id:
        variables["parentId"] = str(args.parent_id)
    print(json.dumps(monday_api(q, variables), indent=2))


def cmd_change_status(args):
    q = """
    mutation ($itemId: ID!, $boardId: ID!, $columnId: String!, $value: JSON!) {
      change_column_value(item_id: $itemId, board_id: $boardId, column_id: $columnId, value: $value) { id }
    }"""
    variables = {
        "itemId": str(args.item_id),
        "boardId": str(args.board_id),
        "columnId": args.column_id,
        "value": json.dumps({"label": args.label}),
    }
    print(json.dumps(monday_api(q, variables), indent=2))


def cmd_query(args):
    print(json.dumps(monday_api(args.graphql), indent=2))


def main():
    p = argparse.ArgumentParser(description="Monday.com GraphQL client (BYOA agent token)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("me").set_defaults(fn=cmd_me)

    gi = sub.add_parser("get-item")
    gi.add_argument("--item-id", required=True)
    gi.set_defaults(fn=cmd_get_item)

    cu = sub.add_parser("create-update")
    cu.add_argument("--item-id", required=True)
    cu.add_argument("--body", required=True)
    cu.add_argument("--parent-id", default=None)
    cu.set_defaults(fn=cmd_create_update)

    cs = sub.add_parser("change-status")
    cs.add_argument("--item-id", required=True)
    cs.add_argument("--board-id", required=True)
    cs.add_argument("--column-id", required=True)
    cs.add_argument("--label", required=True)
    cs.set_defaults(fn=cmd_change_status)

    qy = sub.add_parser("query")
    qy.add_argument("--graphql", required=True)
    qy.set_defaults(fn=cmd_query)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
