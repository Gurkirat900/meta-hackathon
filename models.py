# =============================================================================
# models.py
# =============================================================================
# Think of this file as defining two things:
#
#   1. OBSERVATION — What the AI "sees" (like the screen in a video game)
#   2. ACTION      — What the AI can "do" (like pressing buttons)
#
# We use Pydantic which just means: Python classes that auto-validate data.
# If you give the wrong type, it yells at you immediately. Very helpful.
# =============================================================================

from typing import Optional
from pydantic import Field
from openenv.core.env_server.types import Action, Observation


# =============================================================================
# CANDIDATE MODEL
# =============================================================================
# This is NOT an Action or Observation — it's just a helper class.
# Think of it as a "resume card" that holds one candidate's info.
# We use it inside our Observation below.
# =============================================================================

class Candidate(Observation):
    """Represents one job applicant / resume."""

    candidate_id: str = Field(
        ...,
        description="Unique ID for this candidate, e.g. 'candidate_1'"
    )
    name: str = Field(
        ...,
        description="Candidate's full name"
    )
    years_of_experience: float = Field(
        ...,
        description="Total years of relevant work experience"
    )
    education_level: str = Field(
        ...,
        description="Highest degree: 'high_school', 'bachelors', 'masters', 'phd'"
    )
    education_field: str = Field(
        ...,
        description="What they studied, e.g. 'Computer Science', 'Marketing'"
    )
    skills: list[str] = Field(
        ...,
        description="List of skills they have, e.g. ['Python', 'SQL', 'Excel']"
    )
    previous_roles: list[str] = Field(
        ...,
        description="Job titles they've had before, e.g. ['Junior Developer', 'Intern']"
    )
    has_gap_in_employment: bool = Field(
        default=False,
        description="True if there's a suspicious gap in their work history"
    )
    red_flags: list[str] = Field(
        default_factory=list,
        description="Any red flags in resume, e.g. ['Job hopping', 'Unverifiable degree']"
    )


# =============================================================================
# JOB POSTING MODEL
# =============================================================================
# Represents a job that a company is hiring for.
# Also a helper class used inside Observation below.
# =============================================================================

class JobPosting(Observation):
    """Represents a job opening that candidates are applying for."""

    job_id: str = Field(
        ...,
        description="Unique ID for this job posting, e.g. 'job_42'"
    )
    title: str = Field(
        ...,
        description="Job title, e.g. 'Senior Data Scientist'"
    )
    department: str = Field(
        ...,
        description="Which team, e.g. 'Engineering', 'Marketing', 'Finance'"
    )
    required_skills: list[str] = Field(
        ...,
        description="Skills the candidate MUST have"
    )
    preferred_skills: list[str] = Field(
        ...,
        description="Nice-to-have skills (not mandatory)"
    )
    min_years_experience: float = Field(
        ...,
        description="Minimum years of experience required"
    )
    required_education: str = Field(
        ...,
        description="Minimum education level required"
    )
    description: str = Field(
        ...,
        description="Full text description of the job role and responsibilities"
    )


# =============================================================================
# OBSERVATION — What the AI sees at any moment
# =============================================================================
# Every time the AI looks at the environment, it receives one of these.
# It contains:
#   - The current task name (so AI knows what to do)
#   - The job posting
#   - One or more candidate resumes
#   - Feedback from the last action (empty at start)
#   - Current score so far
# =============================================================================

class ResumeObservation(Observation):
    """
    What the AI agent sees each step.

    Like a 'screen' — everything the agent needs to make a decision.
    """

    # Which of our 3 tasks is active right now
    task_name: str = Field(
        ...,
        description=(
            "Which task to solve: "
            "'match_resume_to_job' | 'rank_candidates' | 'full_screening_report'"
        )
    )

    # The job that needs to be filled
    job: JobPosting = Field(
        ...,
        description="The job posting the candidates are applying for"
    )

    # One or more resumes (Task 1 = 1 resume, Task 2 = 5 resumes, Task 3 = 1 resume)
    candidates: list[Candidate] = Field(
        ...,
        description="List of candidates. Task 1 & 3 have 1 candidate, Task 2 has 5."
    )

    # After the AI takes an action, we send feedback here
    feedback: str = Field(
        default="",
        description="Feedback from last action. Empty at the start of episode."
    )

    # Running score for this episode
    score: float = Field(
        default=0.0,
        description="Score so far in this episode. Starts at 0.0, max is 1.0"
    )

    # Which step number we're on (starts at 0)
    step: int = Field(
        default=0,
        description="How many steps have been taken in this episode"
    )

    # Is this episode finished?
    done: bool = Field(
        default=False,
        description="True when the episode is complete"
    )


# =============================================================================
# ACTION — What the AI can do
# =============================================================================
# The AI sends one of these back to the environment.
# It has fields for all 3 tasks. The AI only fills in what's relevant
# for the current task — the rest can be left empty/None.
# =============================================================================

class ResumeAction(Action):
    """
    What the AI agent sends back as its decision.

    Think of this as the AI "filling out a form" with its answers.
    Different tasks use different fields of this form.
    """

    # Always required — tells us which task this action is for
    task_name: str = Field(
        ...,
        description=(
            "Which task you're answering for: "
            "'match_resume_to_job' | 'rank_candidates' | 'full_screening_report'"
        )
    )

    # ---- TASK 1 FIELD ----
    # For Task 1: "qualified" or "not_qualified"
    decision: Optional[str] = Field(
        default=None,
        description=(
            "Task 1 & 3: Your hire/no-hire decision. "
            "Must be 'qualified' or 'not_qualified'."
        )
    )

    # ---- TASK 2 FIELD ----
    # For Task 2: list of candidate IDs from best to worst fit
    ranking: Optional[list[str]] = Field(
        default=None,
        description=(
            "Task 2 only: List of candidate_ids ordered best fit → worst fit. "
            "Example: ['candidate_3', 'candidate_1', 'candidate_5', ...]"
        )
    )

    # ---- TASK 3 FIELDS ----
    # For Task 3: full report with multiple components
    matched_skills: Optional[list[str]] = Field(
        default=None,
        description="Task 3: Skills from job requirements that the candidate HAS"
    )
    missing_skills: Optional[list[str]] = Field(
        default=None,
        description="Task 3: Required skills the candidate is MISSING"
    )
    identified_red_flags: Optional[list[str]] = Field(
        default=None,
        description="Task 3: Any red flags you noticed in the resume"
    )
    interview_recommended: Optional[bool] = Field(
        default=None,
        description="Task 3: Should this candidate be called for interview?"
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Task 3: How confident are you? 0.0 = not sure, 1.0 = very sure"
    )
