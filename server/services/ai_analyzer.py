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
       - Rate the resume on a scale of 1 to 10 based on relevance to the target role/JD.
       - Identify technical and psychological gaps.

    2. STRATEGIC OPTIMIZATION
       - **CRITICAL REQUIREMENT:** The optimized output must target an 8.5/10+ rating.
       - Transform basic job descriptions into compelling achievement statements (XYZ formula).
       - Implement strategic content hierarchy.
       - Apply advanced optimization (keyword density, action verbs, quantification).

    3. DELIVERABLES CREATION (Mapped to JSON Output)
       - providing actionable feedback.
       - identifying missing skills.
       - creating optimized bullet points using the XYZ formula (Accomplished X by doing Y resulting in Z).
    </Instructions>

    <Constraints>
    - Maintain truthfulness.
    - Advice must be actionable.
    - Final output must be strictly valid JSON.
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
      "overall_score": <int, 0-100, based on the Initial Assessment>,
      "strengths": [<list of strings, key strong points identified>],
      "weaknesses": [<list of strings, critical gaps or weak areas>],
      "ats_issues": [<list of strings, specific formatting or keyword issues causing rejection>],
      "role_alignment_feedback": "<string, specific analysis of how well the candidate fits the target role and what bridges the gap>",
      "optimized_bullets": [<list of strings, rewrite 3-4 key bullet points using the XYZ formula and strong action verbs>],
      "missing_skills": [<list of strings, critical keywords from the JD or Industry Standards that are missing>],
      "final_suggestions": "<string, summary of the Strategic Assessment and Implementation Guidance>",
      "optimized_resume_content": "<string, THE COMPLETE RESTRUCTURED RESUME IN MARKDOWN FORMAT. Follow this structure strictly:\n\n# NAME\n**Title** | **Location** | **Links**\n\n## SUMMARY\n(Paragraph)\n\n## EXPERIENCE\n**Role** at **Company** (Date Range)\n* Bullet point...\n\n## PROJECTS\n**Title** (Technologies used)\n* Bullet point...\n\n## SKILLS\n* **Category**: Skills...\n\n## EDUCATION\n**Degree** | **University** (Dates)\n\nDo NOT use code blocks.>"
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
