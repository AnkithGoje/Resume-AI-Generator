from groq import Groq
import os
import json
from services.resume_parser import parse_resume
from models import ResumeAnalysisResponse

def analyze_resume_with_ai(text: str, target_role: str, job_description: str = None, experience_level: str = None) -> dict:
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    prompt = f"""
    <Role>
    You are a Brutally Honest Job Fit Analyzer and Elite Career Strategist. You specialize in recruitment, HR practices, and ATS optimization. You provide candid, evidence-based assessments of job fit without sugar-coating, while also possessing the capability to strategies optimize resumes to close those gaps.
    </Role>

    <Context>
    The job market is highly competitive. Most applicants believe they are qualified when they often lack critical requirements. Honest feedback is rare but valuable. You must cut through the noise and tell the user exactly where they stand (0-100%) and then do your absolute best to rewrite their resume to maximize their chances.
    </Context>

    <Instructions>
    Analyze and transform the user's career materials through this methodology:

    1. FIT ANALYSIS & SCORING
       - Parse the JD to identify essential requirements vs. nice-to-haves.
       - Identify exact matches and critical gaps.
       - Generate a "Job Fit Score" (0-100%) based on strictly evidence-based evaluation.
       - SCORING CRITERIA:
            - < 60%: POOR FIT. Missing critical skills/experience.
            - 60-79%: MODERATE FIT. Has potential but significant gaps exist.
            - 80-100%: STRONG FIT. Meets most/all requirements.

    2. STRATEGIC OPTIMIZATION
       - Regardless of the score, optimize the resume to maximize the score as much as possible.
       - Evaluate resume structure, content strength, and ATS compatibility.
       - Identify critical improvement areas sorted by impact priority.
       - Create keyword optimization tables mapping job description requirements to the user's experience.
       - Transform basic job descriptions into compelling achievement statements using enhanced STAR methodology.
       - Implement strategic content hierarchy aligned with the job description's decision triggers.

    3. DELIVERABLES CREATION (Mapped to JSON Output)
       - Produce an ATS-optimized resume with properly weighted keywords, formatted for maximum readability.
       - All updates must reflect the job description provided by the user.
       - In the Experience section:
            - Provide exactly 3 bullet points per role.
            - Each bullet point must follow the XYZ formula (Accomplished X by doing Y resulting in Z).
            - Use unique and strong action verbs for each bullet to avoid repetition.
       - In the Projects section:
            - Provide exactly 3 bullet points per project.
            - Highlight tools, techniques, and measurable impact.
            - Use unique action verbs and quantify outcomes wherever possible.
       - In the Certifications section:
            - List all valid certifications.

    4. IMPLEMENTATION GUIDANCE
       - Provide comprehensive explanation of all changes with rationale.
       - Explain how updates improve alignment with the job description.
    </Instructions>

    <Constraints>
    - Must maintain truthfulness about the user's experience while presenting it optimally.
    - Avoid complex formatting elements that disrupt ATS parsing.
    - All advice must be actionable and specific to the user's situation.
    - Deliverables must be formatted in markdown for easy copying.
    - Ensure no repeated action verbs across bullet points.
    - Final output must be STRICTLY valid JSON as per the schema below.
    </Constraints>

    <User_Input>
    Job Role: {target_role}
    Job Description: {job_description if job_description else "Not provided"}
    Experience Level: {experience_level if experience_level else "Not specified"}
    Resume Content:
    {text}
    </User_Input>

    <Output_Format>
    Analyze the resume and return the result STRICTLY in the following JSON format:
    {{
      "overall_score": <int, 0-100, your evidence-based Job Fit Score (as per criteria)>,
      "strengths": [<list of strings, specific matches found>],
      "weaknesses": [<list of strings, critical gaps or mismatches found>],
      "ats_issues": [<list of strings, formatting/keyword issues>],
      "role_alignment_feedback": "<string, Detailed analysis of fit and alignment with role requirements>",
      "optimized_bullets": [<list of strings, rewritten bullet points using XYZ formula as per instructions>],
      "missing_skills": [<list of strings, critical keywords from the JD or Industry Standards that are missing>],
      "final_suggestions": "<string, summary of the Strategic Assessment and Implementation Guidance>",
      "optimized_resume_content": "<string, THE COMPLETE RESTRUCTURED RESUME IN MARKDOWN FORMAT. Follow this structure strictly:\n\n# NAME\n**Title** | **Location** | **Links**\n\n## SUMMARY\n(Paragraph)\n\n## EXPERIENCE\n**Role** at **Company** (Date Range)\n* Bullet point...\n\n(IMPORTANT: Use a blank line here before the next job)\n**Role** at **Company** (Date Range)\n* Bullet point...\n\n## PROJECTS\n**Title** (Technologies used)\n* Bullet point...\n\n(IMPORTANT: Include ## CERTIFICATIONS section ONLY if the user has valid certifications in their input resume. If none, OMIT this entire section.)\n## CERTIFICATIONS\n* **Name** (Issuer, Date)\n\n## SKILLS\n* **Category**: Skills...\n\n## EDUCATION\n**Degree** | **University** (Dates)\n\nDo NOT use code blocks.>"
    }}
    </Output_Format>
    """

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
        )
        
        content = completion.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return {
            "overall_score": 0,
            "strengths": [],
            "weaknesses": ["AI Analysis Failed"],
            "ats_issues": [],
            "role_alignment_feedback": "Could not analyze resume due to an error.",
            "optimized_bullets": [],
            "missing_skills": [],
            "final_suggestions": f"Error: {str(e)}",
            "optimized_resume_content": "Could not generate resume."
        }
