# =============================================================================
# data.py
# =============================================================================
# This file is like a "fake HR database".
# It creates pretend job postings and resumes so the AI has something to work with.
#
# WHY fake data? Because:
#   1. We don't have real candidate data (privacy!)
#   2. We KNOW the correct answers since we made up the data ourselves
#   3. This makes grading 100% possible — we control the "ground truth"
#
# Think of it like a teacher making up math problems — they know the answers
# because they wrote the questions.
# =============================================================================

import random
from models import Candidate, JobPosting


# =============================================================================
# SEED — makes randomness reproducible
# =============================================================================
# If we set random.seed(42), every time you run this file you get the EXACT
# same "random" data. This is important so judges can reproduce our results.
# =============================================================================
RANDOM_SEED = 42


# =============================================================================
# JOBS DATABASE
# =============================================================================
# A list of fake job postings. Each is a plain Python dict.
# We'll convert them to JobPosting objects when needed.
# =============================================================================

JOBS_DATA = [
    {
        "job_id": "job_001",
        "title": "Junior Python Developer",
        "department": "Engineering",
        "required_skills": ["Python", "Git", "SQL"],
        "preferred_skills": ["FastAPI", "Docker", "REST APIs"],
        "min_years_experience": 1.0,
        "required_education": "bachelors",
        "description": (
            "We're looking for a junior developer to join our backend team. "
            "You'll write Python services, work with databases, and collaborate "
            "on REST APIs. Computer Science background preferred."
        )
    },
    {
        "job_id": "job_002",
        "title": "Senior Data Scientist",
        "department": "Data",
        "required_skills": ["Python", "Machine Learning", "Statistics", "SQL"],
        "preferred_skills": ["PyTorch", "Spark", "Kubernetes", "PhD"],
        "min_years_experience": 5.0,
        "required_education": "masters",
        "description": (
            "Join our data science team to build ML models at scale. "
            "You'll design experiments, lead junior data scientists, and "
            "present insights to executives. PhD is a plus."
        )
    },
    {
        "job_id": "job_003",
        "title": "Marketing Manager",
        "department": "Marketing",
        "required_skills": ["Campaign Management", "Analytics", "Copywriting"],
        "preferred_skills": ["SEO", "Google Ads", "HubSpot", "A/B Testing"],
        "min_years_experience": 3.0,
        "required_education": "bachelors",
        "description": (
            "Lead marketing campaigns for our B2B SaaS product. "
            "You'll manage a team of 3, own our content strategy, "
            "and report directly to the CMO."
        )
    },
    {
        "job_id": "job_004",
        "title": "DevOps Engineer",
        "department": "Infrastructure",
        "required_skills": ["Docker", "Kubernetes", "CI/CD", "Linux"],
        "preferred_skills": ["Terraform", "AWS", "Python", "Monitoring"],
        "min_years_experience": 3.0,
        "required_education": "bachelors",
        "description": (
            "Own our cloud infrastructure on AWS. You'll build CI/CD pipelines, "
            "manage Kubernetes clusters, and ensure 99.9% uptime. "
            "On-call rotation required."
        )
    },
    {
        "job_id": "job_005",
        "title": "HR Business Partner",
        "department": "Human Resources",
        "required_skills": ["Recruitment", "Employee Relations", "HRIS"],
        "preferred_skills": ["Workday", "Conflict Resolution", "Employment Law"],
        "min_years_experience": 4.0,
        "required_education": "bachelors",
        "description": (
            "Partner with business leaders to support talent strategy. "
            "Handle performance reviews, onboarding, and employee relations issues. "
            "HR certification is a strong plus."
        )
    }
]


# =============================================================================
# CANDIDATES DATABASE
# =============================================================================
# A large pool of fake candidates.
# Each candidate has a "ground_truth_scores" field (hidden from AI).
# This tells us how well they actually fit each job.
# We use this to grade the AI's decisions.
# =============================================================================

CANDIDATES_DATA = [

    # ----- Great candidates -----

    {
        "candidate_id": "candidate_001",
        "name": "Aisha Patel",
        "years_of_experience": 6.0,
        "education_level": "masters",
        "education_field": "Computer Science",
        "skills": ["Python", "Machine Learning", "Statistics", "SQL", "PyTorch", "Spark"],
        "previous_roles": ["Data Scientist", "ML Engineer"],
        "has_gap_in_employment": False,
        "red_flags": [],
        # Ground truth: how good is this candidate for each job (hidden from AI)
        # Format: { job_id: score }  where 1.0 = perfect, 0.0 = terrible
        "_ground_truth_job_fit": {
            "job_001": 0.5,   # Overqualified for junior dev role
            "job_002": 1.0,   # Perfect for senior data scientist
            "job_003": 0.1,   # Wrong field entirely
            "job_004": 0.3,   # Some overlap but missing DevOps skills
            "job_005": 0.0,   # Completely wrong field
        }
    },

    {
        "candidate_id": "candidate_002",
        "name": "Marcus Thompson",
        "years_of_experience": 2.0,
        "education_level": "bachelors",
        "education_field": "Computer Science",
        "skills": ["Python", "SQL", "Git", "FastAPI", "REST APIs"],
        "previous_roles": ["Junior Developer", "Intern"],
        "has_gap_in_employment": False,
        "red_flags": [],
        "_ground_truth_job_fit": {
            "job_001": 0.95,  # Almost perfect for junior dev
            "job_002": 0.2,   # Not enough experience for senior
            "job_003": 0.0,
            "job_004": 0.3,
            "job_005": 0.0,
        }
    },

    {
        "candidate_id": "candidate_003",
        "name": "Sofia Garcia",
        "years_of_experience": 5.0,
        "education_level": "bachelors",
        "education_field": "Marketing",
        "skills": ["Campaign Management", "Analytics", "Copywriting", "SEO", "HubSpot", "A/B Testing"],
        "previous_roles": ["Marketing Manager", "Campaign Lead", "Marketing Coordinator"],
        "has_gap_in_employment": False,
        "red_flags": [],
        "_ground_truth_job_fit": {
            "job_001": 0.0,
            "job_002": 0.0,
            "job_003": 1.0,   # Perfect for Marketing Manager
            "job_004": 0.0,
            "job_005": 0.2,
        }
    },

    {
        "candidate_id": "candidate_004",
        "name": "Raj Mehta",
        "years_of_experience": 4.0,
        "education_level": "bachelors",
        "education_field": "Computer Science",
        "skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS", "Terraform", "Python"],
        "previous_roles": ["DevOps Engineer", "Site Reliability Engineer"],
        "has_gap_in_employment": False,
        "red_flags": [],
        "_ground_truth_job_fit": {
            "job_001": 0.5,
            "job_002": 0.2,
            "job_003": 0.0,
            "job_004": 1.0,   # Perfect for DevOps
            "job_005": 0.0,
        }
    },

    {
        "candidate_id": "candidate_005",
        "name": "Priya Sharma",
        "years_of_experience": 6.0,
        "education_level": "masters",
        "education_field": "Human Resources",
        "skills": ["Recruitment", "Employee Relations", "HRIS", "Workday", "Employment Law"],
        "previous_roles": ["HR Business Partner", "HR Manager", "Recruiter"],
        "has_gap_in_employment": False,
        "red_flags": [],
        "_ground_truth_job_fit": {
            "job_001": 0.0,
            "job_002": 0.0,
            "job_003": 0.15,
            "job_004": 0.0,
            "job_005": 1.0,   # Perfect for HR Business Partner
        }
    },

    # ----- Medium candidates (partial matches) -----

    {
        "candidate_id": "candidate_006",
        "name": "James Wu",
        "years_of_experience": 1.5,
        "education_level": "bachelors",
        "education_field": "Information Technology",
        "skills": ["Python", "Git", "HTML", "CSS"],   # Missing SQL!
        "previous_roles": ["Intern", "Freelance Developer"],
        "has_gap_in_employment": False,
        "red_flags": [],
        "_ground_truth_job_fit": {
            "job_001": 0.65,  # Good but missing SQL
            "job_002": 0.05,
            "job_003": 0.0,
            "job_004": 0.15,
            "job_005": 0.0,
        }
    },

    {
        "candidate_id": "candidate_007",
        "name": "Fatima Al-Hassan",
        "years_of_experience": 3.5,
        "education_level": "masters",
        "education_field": "Statistics",
        "skills": ["Python", "Statistics", "SQL", "R"],  # Missing ML!
        "previous_roles": ["Data Analyst", "Business Analyst"],
        "has_gap_in_employment": False,
        "red_flags": [],
        "_ground_truth_job_fit": {
            "job_001": 0.4,
            "job_002": 0.55,  # Good stats but missing ML experience & years
            "job_003": 0.2,
            "job_004": 0.0,
            "job_005": 0.2,
        }
    },

    {
        "candidate_id": "candidate_008",
        "name": "Lucas Oliveira",
        "years_of_experience": 4.0,
        "education_level": "bachelors",
        "education_field": "Marketing",
        "skills": ["Campaign Management", "Copywriting", "Google Ads"],  # Missing Analytics
        "previous_roles": ["Marketing Specialist", "Content Creator"],
        "has_gap_in_employment": True,   # Has a gap!
        "red_flags": ["2-year employment gap (2021-2023)"],
        "_ground_truth_job_fit": {
            "job_001": 0.0,
            "job_002": 0.0,
            "job_003": 0.6,   # Decent but missing analytics + has gap
            "job_004": 0.0,
            "job_005": 0.15,
        }
    },

    # ----- Weak / unqualified candidates -----

    {
        "candidate_id": "candidate_009",
        "name": "Tom Wilson",
        "years_of_experience": 0.5,
        "education_level": "high_school",
        "education_field": "General Studies",
        "skills": ["Excel", "Word", "Customer Service"],
        "previous_roles": ["Retail Associate"],
        "has_gap_in_employment": False,
        "red_flags": ["No relevant degree", "No technical skills"],
        "_ground_truth_job_fit": {
            "job_001": 0.0,
            "job_002": 0.0,
            "job_003": 0.1,
            "job_004": 0.0,
            "job_005": 0.15,
        }
    },

    {
        "candidate_id": "candidate_010",
        "name": "Nina Kowalski",
        "years_of_experience": 8.0,
        "education_level": "phd",
        "education_field": "Physics",
        "skills": ["MATLAB", "LaTeX", "Research", "Python"],
        "previous_roles": ["Research Scientist", "Postdoc Researcher"],
        "has_gap_in_employment": False,
        "red_flags": ["No industry experience", "Overqualified for most roles"],
        "_ground_truth_job_fit": {
            "job_001": 0.3,
            "job_002": 0.7,   # Strong but no industry ML experience
            "job_003": 0.0,
            "job_004": 0.1,
            "job_005": 0.0,
        }
    },
]


# =============================================================================
# TASK SCENARIOS
# =============================================================================
# These are pre-defined "quiz questions" for each task.
# Each scenario has:
#   - The inputs (job + candidate(s))
#   - The correct answer (ground truth, hidden from AI)
#
# We hardcode these so results are always reproducible.
# =============================================================================

# Task 1 scenarios: one candidate, one job, answer is qualified/not
TASK1_SCENARIOS = [
    {
        "scenario_id": "t1_easy_1",
        "job_id": "job_001",
        "candidate_id": "candidate_002",
        "correct_decision": "qualified",       # Marcus is perfect for junior dev
        "explanation": "Candidate meets all requirements: Python, SQL, Git, 2yr exp, CS degree"
    },
    {
        "scenario_id": "t1_easy_2",
        "job_id": "job_001",
        "candidate_id": "candidate_009",
        "correct_decision": "not_qualified",   # Tom has no relevant skills
        "explanation": "Candidate has no required skills and only high school education"
    },
    {
        "scenario_id": "t1_medium_1",
        "job_id": "job_002",
        "candidate_id": "candidate_007",
        "correct_decision": "not_qualified",   # Fatima missing ML and experience
        "explanation": "Candidate has stats background but missing ML skills and 1.5yr short on experience"
    },
    {
        "scenario_id": "t1_medium_2",
        "job_id": "job_003",
        "candidate_id": "candidate_008",
        "correct_decision": "not_qualified",   # Lucas has a gap + missing analytics
        "explanation": "Candidate missing Analytics skill and has 2-year employment gap"
    },
    {
        "scenario_id": "t1_hard_1",
        "job_id": "job_001",
        "candidate_id": "candidate_006",
        "correct_decision": "not_qualified",   # James missing SQL (required!)
        "explanation": "SQL is required but candidate only has Python and Git"
    },
]

# Task 2 scenarios: 5 candidates for 1 job, answer is correct ranking order
TASK2_SCENARIOS = [
    {
        "scenario_id": "t2_main",
        "job_id": "job_002",   # Senior Data Scientist
        "candidate_ids": [
            "candidate_001",   # Aisha  - perfect fit (1st)
            "candidate_010",   # Nina   - strong but no industry ML (2nd)
            "candidate_007",   # Fatima - partial match (3rd)
            "candidate_002",   # Marcus - dev not data scientist (4th)
            "candidate_009",   # Tom    - completely unqualified (5th)
        ],
        # The CORRECT ranking from best to worst
        "correct_ranking": [
            "candidate_001",
            "candidate_010",
            "candidate_007",
            "candidate_002",
            "candidate_009",
        ]
    }
]

# Task 3 scenarios: one candidate, full report expected
TASK3_SCENARIOS = [
    {
        "scenario_id": "t3_main",
        "job_id": "job_002",           # Senior Data Scientist
        "candidate_id": "candidate_010",  # Nina - interesting edge case
        "correct_decision": "qualified",  # Technically yes, with caveats
        "correct_matched_skills": ["Python", "Statistics"],   # Has these
        "correct_missing_skills": ["Machine Learning", "SQL"],  # Missing these
        "correct_red_flags": ["No industry experience"],
        "interview_should_be_recommended": True,
        "explanation": (
            "Nina is a PhD physicist with Python and stats but no direct ML/SQL experience. "
            "She's borderline — smart enough but untested in industry. "
            "Recommend interview to assess adaptability."
        )
    }
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
# These functions convert our plain dicts into proper model objects.
# Think of them as "assemblers" — they take raw ingredients and build the product.
# =============================================================================

def get_job(job_id: str) -> JobPosting:
    """
    Look up a job by ID and return it as a JobPosting object.

    Example:
        job = get_job("job_001")
        print(job.title)  # "Junior Python Developer"
    """
    job_dict = next((j for j in JOBS_DATA if j["job_id"] == job_id), None)

    if job_dict is None:
        raise ValueError(f"Job '{job_id}' not found in database.")

    # Remove private fields before building the object
    clean = {k: v for k, v in job_dict.items() if not k.startswith("_")}
    return JobPosting(**clean)


def get_candidate(candidate_id: str) -> Candidate:
    """
    Look up a candidate by ID and return a Candidate object.
    Private fields (starting with _) are stripped — AI won't see ground truth.

    Example:
        c = get_candidate("candidate_001")
        print(c.name)  # "Aisha Patel"
    """
    candidate_dict = next(
        (c for c in CANDIDATES_DATA if c["candidate_id"] == candidate_id), None
    )

    if candidate_dict is None:
        raise ValueError(f"Candidate '{candidate_id}' not found in database.")

    # Strip private fields so AI can't cheat
    clean = {k: v for k, v in candidate_dict.items() if not k.startswith("_")}
    return Candidate(**clean)


def get_candidate_fit_score(candidate_id: str, job_id: str) -> float:
    """
    Returns the hidden ground-truth fit score for a candidate/job pair.
    Used ONLY by the grader — never shown to AI.

    Returns a float from 0.0 (terrible fit) to 1.0 (perfect fit).
    """
    candidate_dict = next(
        (c for c in CANDIDATES_DATA if c["candidate_id"] == candidate_id), None
    )

    if candidate_dict is None:
        raise ValueError(f"Candidate '{candidate_id}' not found.")

    fit_scores = candidate_dict.get("_ground_truth_job_fit", {})
    return fit_scores.get(job_id, 0.0)


def get_task1_scenario(scenario_id: str = None) -> dict:
    """
    Get a Task 1 scenario by ID, or a random one if no ID given.

    Returns the full scenario dict including correct_decision.
    """
    if scenario_id:
        scenario = next(
            (s for s in TASK1_SCENARIOS if s["scenario_id"] == scenario_id), None
        )
        if scenario is None:
            raise ValueError(f"Scenario '{scenario_id}' not found.")
        return scenario

    # Random but reproducible
    random.seed(RANDOM_SEED)
    return random.choice(TASK1_SCENARIOS)


def get_task2_scenario(scenario_id: str = None) -> dict:
    """
    Get a Task 2 scenario by ID, or default one.
    """
    if scenario_id:
        scenario = next(
            (s for s in TASK2_SCENARIOS if s["scenario_id"] == scenario_id), None
        )
        if scenario is None:
            raise ValueError(f"Scenario '{scenario_id}' not found.")
        return scenario

    return TASK2_SCENARIOS[0]


def get_task3_scenario(scenario_id: str = None) -> dict:
    """
    Get a Task 3 scenario by ID, or default one.
    """
    if scenario_id:
        scenario = next(
            (s for s in TASK3_SCENARIOS if s["scenario_id"] == scenario_id), None
        )
        if scenario is None:
            raise ValueError(f"Scenario '{scenario_id}' not found.")
        return scenario

    return TASK3_SCENARIOS[0]


# =============================================================================
# QUICK TEST — Run this file directly to verify everything works
# Usage: python data.py
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DATA.PY — Quick Test")
    print("=" * 60)

    # Test job lookup
    job = get_job("job_001")
    print(f"\n✅ Job loaded: {job.title} ({job.department})")
    print(f"   Required skills: {job.required_skills}")
    print(f"   Min experience: {job.min_years_experience} years")

    # Test candidate lookup
    candidate = get_candidate("candidate_001")
    print(f"\n✅ Candidate loaded: {candidate.name}")
    print(f"   Experience: {candidate.years_of_experience} years")
    print(f"   Skills: {candidate.skills}")
    print(f"   Red flags: {candidate.red_flags or 'None'}")

    # Test fit score (hidden from AI)
    score = get_candidate_fit_score("candidate_001", "job_002")
    print(f"\n✅ Fit score (Aisha for Senior Data Scientist): {score}")

    score2 = get_candidate_fit_score("candidate_009", "job_002")
    print(f"✅ Fit score (Tom for Senior Data Scientist): {score2}")

    # Test scenario loading
    scenario = get_task1_scenario("t1_easy_1")
    print(f"\n✅ Task 1 scenario: {scenario['scenario_id']}")
    print(f"   Correct answer: {scenario['correct_decision']}")
    print(f"   Reason: {scenario['explanation']}")

    scenario2 = get_task2_scenario()
    print(f"\n✅ Task 2 scenario: {scenario2['scenario_id']}")
    print(f"   Candidates to rank: {scenario2['candidate_ids']}")
    print(f"   Correct ranking: {scenario2['correct_ranking']}")

    print("\n✅ All data loaded successfully!")
