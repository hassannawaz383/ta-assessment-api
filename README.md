# ta-assessment-api

Backend service for handling recruitment assessment submissions.

The purpose of this project is to provide a reliable API where candidates can access their assigned assessment, submit their work, and where HR reviewers can review submissions, score candidates, and maintain an audit trail of important actions.

The project focuses on clean API design, authentication, validation, database relationships, and reliability considerations rather than only basic CRUD operations.


# Tech Stack

Python
Django
Django REST Framework
PostgreSQL
JWT Authentication
DRF Spectacular (OpenAPI documentation)


# Main Features

## Candidate Workflow

Candidates can:

Fetch their assessment brief using a private token
Submit their assessment work
Provide:
  Work link
  File reference
  Time taken
  Notes
  Challenges

The system prevents duplicate submissions for the same candidate and assessment.



## Reviewer Workflow

HR reviewers can:

Authenticate through the API
List assessment submissions
Filter submissions by:
  Role
  Status
  Candidate city
  Submission date
  Score range

Reviewers can also:

Add a score
Add a decision
Add a private review note


## Audit Logging

Important actions are stored in an audit log.

Currently tracked actions:

Submission created
Review added

Each audit record stores:

Submission reference
Actor type
Actor ID
Action performed
Previous data
New data
Timestamp

This allows tracking of important workflow events.


# Project Structure

ta-assessment-api/
│
├── apps/
│   │
│   ├── candidates/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── assessments/
│   │   ├── models.py
│   │   └── tests.py
│   │
│   ├── submissions/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── reviews/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── audit_logs/
│   │   ├── models.py
│   │   └── tests.py
│   │
│   ├── users/
│   │   └── models.py
│   │
│   └── common/
│       ├── authentication.py
│       └── permissions.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── schema.yml
└── README.md



# Database Design

The main database entities are:

## Candidate

Stores candidate information.

Important fields:

Name
Email
City
Private token

The private token is indexed and unique because it is used for candidate authentication.


## AssessmentBrief

Stores assessment information.

Important fields:

Role
Title
Description
Active status

Assessment roles are controlled using predefined choices.



## Submission

Represents a candidate's submitted work.

Important fields:

Candidate
Assessment
Work link
File reference
Time taken
Notes
Challenges
Status
Submitted date

A unique constraint exists on:

candidate + assessment

This prevents the same candidate from submitting multiple times for the same assessment.

Indexes are added for:

Status filtering
Submission date filtering



## Review

Stores reviewer evaluation data.

Important fields:

Submission
Reviewer
Score
Decision
Private note

Each submission can have one review.


## AuditLog

Stores workflow history.

Important fields:

Submission
Actor
Action
Old data
New data
Created timestamp


# Authentication

The project uses two authentication approaches.

## Candidate Authentication

Candidates authenticate using a private token passed through:

X-Candidate-Token

The token is generated per candidate and stored securely in the database.

Invalid or missing tokens are rejected.


## Reviewer Authentication

Reviewers authenticate using JWT tokens.

JWT endpoints are provided for:

Login
Token refresh

Reviewer-only endpoints require authentication before accessing submission review functionality.


# API Endpoints

## Candidate

### Get Assessment Brief

GET

/api/v1/assessment-brief/

Headers:

X-Candidate-Token: candidate_private_token


## Submission

### Create Submission

POST

/api/v1/submissions/

Example request:

{

  "assessment": "assessment_uuid",

  "work_link": "https://github.com/example/project",

  "file_reference": "submission.zip",

  "time_taken_minutes": 240,

  "notes": "Completed backend implementation",

  "challenges": "Handled authentication and validation"

}

Response:

{

  "id": "submission_uuid",

  "status": "PENDING"

}


## Reviewer

### Login

POST

/api/v1/auth/login/

Returns JWT access and refresh tokens.


### List Submissions

GET

/api/v1/reviewer/submissions/

Supported filters:

role
status
city
submitted_after
score_min
score_max

Example:

GET /api/v1/reviewer/submissions/?status=PENDING&city=Lahore


### Add Review

POST

/api/v1/reviewer/submissions/{submission_id}/review/

Example request:

{

  "score": 92,

  "decision": "PASS",

  "private_note": "Good backend design and validation."

}


# Validation and Error Handling

The API handles:

## Missing candidate token

Requests without a candidate token are rejected.

## Invalid candidate token

Invalid tokens return authentication errors.

## Duplicate submission

A candidate cannot submit the same assessment more than once.

The API returns:

409 Conflict

## Invalid review data

Serializer validation prevents invalid scores and decisions from being stored.

## Unauthorized reviewer access

Reviewer endpoints require authentication.


# Query Optimization

Submission listing uses:

select_related()
prefetch_related()

to avoid unnecessary database queries when fetching:

Candidate information
Assessment information
Review information

This prevents common N+1 query problems.


# Background Processing Considerations

Some operations may become expensive as the system grows.

Examples:

## File scanning

Uploaded files should not block the submission request.

A background worker could:

Receive the uploaded file
Scan it asynchronously
Update the submission status after completion

## Email notifications

Candidate and reviewer notifications should be handled through a background queue instead of delaying API responses.

Possible tools:

Celery
Redis
RabbitMQ

## Automated scoring

If AI-based evaluation is introduced, scoring should run asynchronously and store results after processing.


# Handling Large Scale Data

For approximately 50,000 applicants:

The system can scale by:

Adding database indexes on frequently filtered fields
Using pagination for reviewer submission lists
Avoiding unnecessary joins
Moving heavy tasks to background workers
Adding caching for frequently accessed assessment briefs

The submission table can be partitioned or archived in the future if historical data grows significantly.


# Migrations

Database changes are managed through Django migrations.

The migration workflow:

Modify models
Generate migrations
Review migration changes
Apply migrations

Rollback is handled using Django migration rollback commands.


# Environment Variables

Sensitive configuration should not be stored in source control.

Recommended environment variables:

SECRET_KEY
DATABASE_URL
DEBUGG
JWT configuration values


# Running the Project

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create an admin user:

python manage.py createsuperuser

Run development server:

python manage.py runserver


# Running Tests

The project includes tests covering:

Candidate authentication
Invalid candidate token handling
Submission creation
Duplicate submission prevention
Reviewer authentication
Review creation
Audit logging

Run:

python manage.py test


# API Documentation

OpenAPI documentation is generated using DRF Spectacular.

Schema generation:

python manage.py spectacular --file schema.yml

The generated schema can be imported into:

Swagger UI
Postman
Other OpenAPI-compatible tools


# Deployment Notes

For production deployment:

Recommended setup:

Django application server using Gunicorn
PostgreSQL database
Reverse proxy using Nginx
Environment-based configuration
Centralized logging
Automated database backups


# Logging and Monitoring

Production systems should monitor:

API errors
Authentication failures
Slow queries
Background job failures

Logs should avoid storing sensitive candidate information.


# Design Decisions and Tradeoffs

## Why private token authentication for candidates?

Candidates do not need full accounts. A private token provides a simple controlled access mechanism for assessment completion.

## Why JWT for reviewers?

Reviewers require authenticated access to internal workflows, making JWT suitable for session management.

## Why Django ORM constraints?

Database constraints provide an additional layer of protection against duplicate submissions, even if application level validation fails.

## Why simple architecture?

The assessment focuses on reliability and practical backend decisions. The implementation avoids unnecessary complexity while keeping the system extensible.


