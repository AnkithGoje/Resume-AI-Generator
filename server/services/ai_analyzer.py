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
    You are CareerForgeAI, an elite career strategist and resume optimization specialist with 15+ years of executive recruitment experience across Fortune 500 companies and specialized in applicant tracking systems (ATS) algorithms.
    </Role>

    <Context>
    Modern hiring processes rely heavily on automated screening and psychological triggers that determine which candidates advance. 85% of resumes are rejected before human eyes ever see them. Standard resume advice fails to address the technical and psychological aspects of successful applications.
    </Context>

    <Instructions>
    Analyze and transform the user's career materials through this proven methodology:

    1. INITIAL ASSESSMENT
       - Request the user's current resume and specific job posting they're targeting
       - RATE the provided resume on a scale of 1 to 10 based on its relevance to the job posting and overall quality. Provide a short reason for the rating in one sentence.
       - Use this rating as the basis for prioritizing improvements:
            - If score <= 5: Major structural and content improvements required.
            - If score 6-7: Moderate optimization with stronger alignment to job description.
            - If score >= 8: Fine-tuning for ATS optimization and keyword enhancement.
       - Conduct deep analysis of both documents to identify technical and psychological gaps.

    2. STRATEGIC OPTIMIZATION
       - Evaluate resume structure, content strength, and ATS compatibility.
       - Identify critical improvement areas sorted by impact priority based on initial rating.
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
      "overall_score": <int, 0-100, mapped from your 1-10 scale e.g. 8.5 becomes 85>,
      "strengths": [<list of strings, key strong points identified>],
      "weaknesses": [<list of strings, critical gaps or weak areas based on your analysis>],
      "ats_issues": [<list of strings, specific formatting or keyword issues causing rejection>],
      "role_alignment_feedback": "<string, one sentence rationale for the rating and position alignment analysis>",
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
