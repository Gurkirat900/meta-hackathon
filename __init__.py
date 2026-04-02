# =============================================================================
# __init__.py
# =============================================================================
# This file has ONE job: tell Python that this folder is a "package"
# (a collection of related Python files that can be imported together).
#
# Without this file, Python wouldn't know that resume_screening_env/
# is a package — it would just look like a random folder.
#
# We also re-export our key classes here so users can do:
#   from resume_screening_env import ResumeAction, ResumeObservation
# Instead of the longer:
#   from resume_screening_env.models import ResumeAction, ResumeObservation
# =============================================================================

from models import ResumeAction, ResumeObservation, Candidate, JobPosting

# What gets exported when someone does: from resume_screening_env import *
__all__ = [
    "ResumeAction",
    "ResumeObservation",
    "Candidate",
    "JobPosting",
]
