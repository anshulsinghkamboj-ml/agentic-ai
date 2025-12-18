```mermaid
flowchart TD

    %% Entry Point
    A[main_async.py<br/>async main()] --> B[retry_with_backoff_async]

    %% LLM Call
    B --> C[get_plan_async<br/>llm_async.py]
    C --> C1[_call_model]
    C1 --> D[OpenAI API]

    %% Timeout Boundary
    C -->|Timeout| E[LLMTimeoutError]

    %% Raw Output
    D --> F[raw_output]
    F --> G[log_event<br/>logger.py]

    %% Validation Loop
    F --> H[validate_plan<br/>validator.py]

    %% JSON Cleaning & Parsing
    H --> H1[_clean_json]
    H1 --> H2[json.loads]

    %% Schema Validation
    H2 --> I[Plan.model_validate<br/>schema.py]

    %% Success Path
    I --> J[PLAN ACCEPTED]
    J --> J1[log validated_plan]
    J --> END[Exit Success]

    %% Validation Failures
    H2 -->|JSONDecodeError| K1
    I -->|ValidationError| K1

    %% Failure Classification
    K1[classify_failure<br/>failures.py]
    E --> K1

    %% Metrics
    K1 --> L[record failure<br/>metrics.py]

    %% Circuit Breaker
    K1 --> M{CircuitBreaker<br/>allow?}
    M -->|No| N[FATAL FAILURE]
    M -->|Yes| O{Failure Type?}

    %% Schema Repair Path
    O -->|SCHEMA_JSON / SCHEMA_VALIDATION| P[repair_plan<br/>llm.py]
    P --> F

    %% Timeout / Connection Path
    O -->|TIMEOUT / CONNECTION| N

    %% Unknown Failure
    O -->|UNKNOWN| N

    %% Logging Fatal
    N --> Q[log fatal_failure]
    Q --> END_FAIL[Exit Failure]
```
