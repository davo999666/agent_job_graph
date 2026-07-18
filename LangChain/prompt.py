from langchain_core.prompts import ChatPromptTemplate


MATCH_PROMPT = ChatPromptTemplate.from_template(
    """
You are a strict CV-job matching assistant.

STRICT RULES:
- Use at most 1000 tokens for the response.
- Use ONLY explicit information from the CV and job description.
- Do NOT guess, infer, or assume missing skills.

OUTPUT FORMAT:
Return ONLY plain text.
Do NOT return JSON.
Do NOT return Markdown.
Do NOT use code fences.

Use exactly this format:

Match: <number>%

Matching skills:
- <skill>
- <skill>
- <skill>

Missing skills:
- <skill>: <what it is>
- <skill>: <what it is>

Reason:
<short explanation>


JOB:
{job_text}

CV:
{cv_text}
"""
)

CV_EXTRACT_PROMPT = ChatPromptTemplate.from_template(
    """
Extract structured information from the CV.

Rules:
- Use only information explicitly written in the CV.
- Do not guess or invent information.
- Remove duplicate values.
- Put each technology in the most appropriate category.
- If information is missing, use an empty string, empty array, or empty object.
- Return only valid JSON.
- Do not include Markdown or explanations.

Return exactly this structure:

{{
  "title": "",
  "years_experience": "",
  "skills": [],
  "technologies": {{
    "programming_languages": [],
    "frontend": [],
    "backend": [],
    "frameworks": [],
    "libraries": [],
    "databases": [],
    "cloud": [],
    "devops_tools": [],
    "ai": [],
    "communication_protocols": [],
    "orms": [],
    "testing": [],
    "messaging": [],
    "caching": [],
    "security": [],
  }},
  "projects": [
    {{
      "name": "",
      "description": "",
    }}
  ],
  "education": []
}}

CV:
{cv_text}
"""
)

JOB_EXTRACT_PROMPT = ChatPromptTemplate.from_template(
    """
Extract structured information from the job description.

Rules:
- Use only information explicitly written in the job description.
- Do not guess or invent information.
- Remove duplicate values.
- Put each technology in the most appropriate category.
- Separate required qualifications from preferred qualifications.
- If information is missing, use an empty string, empty array, or empty object.
- Return only valid JSON.
- Do not include Markdown or explanations.

Return exactly this structure:

{{
  "title": "",
  "company": "",
  "location": "",
  "employment_type": "",
  "work_model": "",
  "experience_required": "",
  "description": "",
  "responsibilities": [],
  "required_skills": [],
  "preferred_skills": [],
  "technologies": {{
    "programming_languages": [],
    "frontend": [],
    "backend": [],
    "frameworks": [],
    "libraries": [],
    "databases": [],
    "cloud": [],
    "devops_tools": [],
    "ai": [],
    "communication_protocols": [],
    "orms": [],
    "testing": [],
    "messaging": [],
    "caching": [],
    "security": [],
  }},
  "education_requirements": [],
  "language_requirements": [],
  "certifications": [],
  "benefits": [],
}}

job_title:
{job_title}

Job description:
{job_description}

"""
)