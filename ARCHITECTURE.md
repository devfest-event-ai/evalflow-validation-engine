# Architecture Decision Log

This document records the architectural decisions made during the development of EvalFlow.

## System Architecture

### Overview

EvalFlow follows a 3-tier architecture:
1. Presentation Layer: Streamlit dashboard
2. Application Layer: FastAPI backend
3. Validation Layer: FMR Scoring Engine

### Diagram

+-----------------+
| Streamlit UI | (Port 8501)
+--------+--------+
|
| HTTP Requests
v
+-----------------+
| FastAPI Server | (Port 8000)
+--------+--------+
|
v
+-----------------+
| FMR Scoring |
| Engine |
+-----------------+


## Decision Records

### Decision 1: FastAPI for Backend

Date: 2026-05-27
Status: Accepted

Context:
Need a high-performance async API framework for clinical data extraction.

Decision:
Use FastAPI instead of Flask or Django REST Framework.

Consequences:
- Pros:
  - Automatic OpenAPI documentation (Swagger UI)
  - Async support for high concurrency
  - Built-in data validation with Pydantic
  - Faster performance
- Cons:
  - Smaller community than Flask/Django
  - Requires Python 3.6+

### Decision 2: Streamlit for Frontend

Date: 2026-05-28
Status: Accepted

Context:
Need a quick, interactive dashboard for demo and testing.

Decision:
Use Streamlit instead of React/Vue/Angular.

Consequences:
- Pros:
  - Rapid development (pure Python)
  - No frontend framework knowledge needed
  - Built-in widgets and components
  - Easy deployment
- Cons:
  - Less customizable than React
  - Not suitable for production-scale UI
  - Limited styling options

### Decision 3: Regex-Based Extraction

Date: 2026-05-27
Status: Accepted

Context:
Need to extract structured data from unstructured clinical notes.

Decision:
Use regex patterns instead of NLP libraries (spaCy, NLTK).

Consequences:
- Pros:
  - No external dependencies
  - Fast execution
  - Easy to understand and debug
  - No ML model training required
- Cons:
  - Less flexible for complex patterns
  - Requires manual pattern updates
  - May miss edge cases

### Decision 4: FMR Confidence Scoring

Date: 2026-05-27
Status: Accepted

Context:
Need a way to validate extraction quality automatically.

Decision:
Implement custom 3-component FMR scoring:
- Completeness (presence of critical fields)
- Pattern Quality (strength of matches)
- Consistency (cross-field validation)

Consequences:
- Pros:
  - Transparent scoring logic
  - Easy to explain to stakeholders
  - Configurable thresholds
  - No external ML dependencies
- Cons:
  - Requires manual threshold tuning
  - May not capture all quality aspects
  - Less sophisticated than ML-based scoring

### Decision 5: Threshold-Based Routing

Date: 2026-05-27
Status: Accepted

Context:
Need automated decision routing for production workflows.

Decision:
Use confidence score thresholds:
- >= 0.7: Approved
- 0.4 - 0.69: Review Required
- < 0.4: Rejected

Consequences:
- Pros:
  - Clear decision boundaries
  - Easy to implement and test
  - Prevents bad data in production
  - Human review for edge cases
- Cons:
  - Thresholds may need adjustment
  - Binary decisions may miss nuance
  - Requires monitoring and tuning

## Technology Choices

### Python 3.11
- Latest stable version
- Performance improvements
- Type hint support

### FastAPI
- Modern async framework
- Automatic validation
- Great documentation

### Streamlit
- Rapid prototyping
- Python-only (no JS/HTML)
- Interactive components

### Pydantic
- Data validation
- Type checking
- Automatic schema

### Git + GitHub
- Version control
- Collaboration
- CI/CD ready

## Future Considerations

### Potential Improvements

1. Database Integration
   - PostgreSQL for persistent storage
   - SQLAlchemy ORM
   - Migration support

2. Authentication
   - JWT tokens
   - User management
   - Role-based access

3. ML-Based Extraction
   - NLP models (spaCy, transformers)
   - Better accuracy for complex notes
   - Continuous learning

4. Microservices Architecture
   - Separate extraction service
   - Separate scoring service
   - Message queue (RabbitMQ/Kafka)

5. Monitoring and Logging
   - Prometheus metrics
   - Grafana dashboards
   - Centralized logging

6. Testing Framework
   - pytest for unit tests
   - Integration tests
   - E2E tests



