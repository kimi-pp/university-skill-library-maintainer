---
name: new-rabbitmq-consumer
description: Scaffold a RabbitMQ consumer and/or publisher in road24-insurance (event-driven flows) — message schema, consumer handler delegating to a service, publishing, and idempotent/retry handling. Use for "react to the X event", "publish Y when Z happens", "add a queue consumer".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
argument-hint: "[event/queue] [what to do]"
---

# Create a RabbitMQ Consumer / Publisher

Messaging for: $ARGUMENTS

`road24-insurance` uses RabbitMQ for event-driven flows (`src/consumers/`, `src/publisher/`,
`src/broker.py`). Use this for reacting to / emitting domain events. For fire-and-forget background
jobs, prefer `new-celery-task` instead.

## Steps

1. **Read first** — `src/broker.py` (connection/exchange/queue setup), an existing consumer in
   `src/consumers/`, and the publisher in `src/publisher/`. Match the message contract + (de)serialization.
2. Define the message schema (Pydantic) so payloads are validated on consume.
3. **Consumer**: thin handler that validates the message → calls a **service** (`execute()`) → acks.
   Keep all logic in the service.
4. **Publisher**: emit the event after the state change commits (avoid publishing then failing to persist).
5. Make handling **idempotent** (dedupe by event id / business key); on transient failure nack/retry,
   on poison messages route to a DLQ — don't infinite-loop.

## Consumer pattern

```python
from src.schemas.events import PolicyConfirmedEvent
from src.services.policy.sync import SyncPolicyService


async def handle_policy_confirmed(message) -> None:
    event = PolicyConfirmedEvent.model_validate_json(message.body)
    await SyncPolicyService(policy_id=event.policy_id).execute()
    await message.ack()
```

## Publisher pattern

```python
await publisher.publish(
    routing_key="policy.confirmed",
    body=PolicyConfirmedEvent(policy_id=policy.id).model_dump_json(),
)
```

## Rules

- Logic in services; consumers/publishers are thin adapters. Validate every incoming message.
- Idempotent consumers (events can be redelivered). Ack only after success; nack/DLQ on failure.
- Publish **after** the DB commit (or use an outbox) so you never emit an event for work that rolled back.
- Don't block the event loop; log via the project logger + `road24-sdk` trace context; never leak PII.
