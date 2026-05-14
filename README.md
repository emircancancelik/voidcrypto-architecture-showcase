# VoidCrypto: Event-Driven Multi-Agent Trading Architecture

## Overview
This repository serves as an architectural showcase for **VoidCrypto**, a highly concurrent, 7-agent AI crypto trading orchestrator deployed on Azure. 

**Note on Proprietary Logic:** This repository contains infrastructure configurations, data contracts, and architectural base classes. The core mathematical models, machine learning pipelines (XGBoost/Deep Learning), and proprietary execution algorithms (Alpha) are strictly omitted to protect intellectual property.

## Architecture & Infrastructure

VoidCrypto is designed around an event-driven, non-blocking asynchronous architecture prioritizing strict type safety and cloud cost optimization.

*   **Compute:** Azure Container Apps
*   **Autoscaling:** KEDA (Kubernetes Event-driven Autoscaling)
*   **Message Broker:** RabbitMQ (Asynchronous triggers & execution payloads)
*   **In-Memory State:** Redis (Agent consensus snapshots & high-frequency order book data)
*   **Language & Validation:** Python 3.10+, `asyncio`, `Pydantic`

### The "Scale-to-Zero" Paradigm
Continuous polling and monolith execution loops are strictly avoided. The heavy-compute agents (Technical Analysis AI, ML Price Action AI, Master Decision AI) and the Risk & Execution AI operate on a `min-replicas: 0` configuration. 

Wake-up events are managed by KEDA observing RabbitMQ queues. When a critical threshold in Redis is crossed, a message is published to the broker. KEDA spins up the required containers within seconds, the agents achieve consensus, dispatch the execution payload to the execution queue, and immediately spin down.

## Agent Topology

The system operates via a distributed consensus among 7 specialized agents:

1.  **Order Book AI:** High-frequency bid/ask spread and liquidity analysis.
2.  **Whale Tracker AI:** On-chain wallet transaction monitoring.
3.  **News/Sentiment AI:** NLP-based real-time sentiment extraction from external APIs (X, Reddit, News Monitors).
4.  **Technical Analysis (TA) AI:** Strictly classification-based (1/0 + confidence) indicator analysis.
5.  **ML Price Action AI:** Machine learning-based candlestick pattern recognition (Classification only).
6.  **Master Decision AI (Orchestrator):** The consensus layer. Aggregates data from Redis, calculates weighted probabilities, and generates strict execution payloads.
7.  **Risk & Execution AI:** 100% deterministic execution layer. Evaluates ATR and order-book math for Trailing Stops and OCO (One-Cancels-the-Other) orders. Contains ZERO machine learning models.

## Core Engineering Principles

*   **Strict Type Safety:** Loose data structures are prohibited. All inter-agent communication, Redis state updates, and RabbitMQ payloads are rigorously validated using `Pydantic` schemas. Invalid payloads result in immediate rejection, preventing execution layer crashes.
*   **Domain-Specific Naming:** Generic variables (`data`, `result`) are banned. All variables adhere to financial and architectural domain language (e.g., `trade_signal`, `atr_14`, `correlation_id`).
*   **Structured Logging:** Standard `print()` functions are explicitly bypassed. All system events use a custom JSON-formatted logger ensuring machine readability and seamless Azure Log Analytics integration.
*   **Fault Tolerance:** The Execution AI does not close trades based on probabilistic ML outputs; exits are strictly governed by deterministic mathematical models.

## Showcase Repository Structure

```text
voidcrypto-architecture-showcase/
├── core/
│   ├── base_agent.py          # Abstract Base Class for all autonomous agents
│   └── consensus_pipeline.py  # Abstraction of the multi-agent consensus flow
├── infrastructure/
│   ├── Dockerfile             # Multi-stage, slimmed build for Azure deployment
│   └── keda-scaler.yaml       # KEDA RabbitMQ trigger configuration
├── schemas/
│   └── data_contracts.py      # Pydantic models (AgentSignal, ExecutionPayload)
├── shared/
│   ├── logging_factory.py     # JSON structured logging implementation
│   └── settings_manager.py    # Type-safe environment variable management
└── README.md
