import json


def new_game():
    return {"items": {}, "load": 0, "capacity": 2, "stock": 100, "metric": 100, "day": 1, "id": 0, "fault": False, "resource": 10, "rate": 2, "clock": 0, "paused": False, "settled": False, "received": []}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state.setdefault("received", [])
    return state


def add(state, item_id, amount):
    if state["settled"]:
        return False
    if item_id in state["items"]:
        return False
    if amount <= 0 or amount > state["stock"]:
        return False
    state["items"][item_id] = amount
    state["stock"] -= amount
    return True


def receive(state, item_id):
    if state["settled"]:
        return False
    if item_id in state["received"]:
        return True
    if state["load"] >= state["capacity"] or item_id not in state["items"]:
        return False
    state["received"].append(item_id)
    state["load"] += 1
    return True


def fee(state, item_id, end_day):
    return max(0, (end_day - state["day"]) * state["rate"])


def cancel(state, item_id):
    if state["settled"] or item_id not in state["items"]:
        return False
    state["stock"] += state["items"].pop(item_id)
    if item_id in state["received"]:
        state["received"].remove(item_id)
        state["load"] -= 1
    return True


def produce(state, amount):
    if state["settled"] or state["fault"] or amount <= 0:
        return False
    return True


def event(state):
    if state["settled"]:
        return state["metric"]
    state["metric"] -= 10
    return state["metric"]


def guard(state, item_id):
    if state["settled"]:
        return False
    return state["resource"] > 0


def tick(state):
    if state["paused"] or state["settled"]:
        return state["clock"]
    state["clock"] += 1
    return state["clock"]


def settle(state):
    state["settled"] = True
    return True


def main():
    print("命令: add/receive/fee/cancel/produce/event/guard/tick/settle/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        try:
            if cmd == "add":
                ok = add(state, int(args[0]), int(args[1]))
            elif cmd == "receive":
                ok = receive(state, int(args[0]))
            elif cmd == "fee":
                print(fee(state, int(args[0]), int(args[1])))
                continue
            elif cmd == "cancel":
                ok = cancel(state, int(args[0]))
            elif cmd == "produce":
                ok = produce(state, int(args[0]))
            elif cmd == "event":
                print(event(state))
                continue
            elif cmd == "guard":
                ok = guard(state, int(args[0]))
            elif cmd == "tick":
                print(tick(state))
                continue
            elif cmd == "settle":
                ok = settle(state)
            else:
                print("未知命令")
                continue
        except (IndexError, ValueError):
            print("参数错误")
            continue
        print("ok" if ok else "fail")


if __name__ == "__main__":
    main()
