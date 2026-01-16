from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.resume_parser import extract_text
from .utils.text_cleaner import clean_text
from .utils.gemini_client import gemini_analyze_resume


def home(request):
    return render(request, 'analyzer/index.html')

@csrf_exempt
def analyze_resume(request):
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        
        if not resume:
            return JsonResponse({'error': 'No file uploaded'})

        text = extract_text(resume)
        text = clean_text(text)

        job_description = request.POST.get("job_description", "").strip()

        ai_result = gemini_analyze_resume(text, job_description)

        # 👉 OPTION A: PYTHON CALCULATES SCORE HERE
        score = calculate_score(
            ai_result["jdMatch"]["missingSkills"],
            ai_result["improvements"],
            ai_result["goodPoints"]
        )

        ai_result["jdMatch"]["score"] = score

        return JsonResponse({
            "success": True,
            **ai_result
        })

    return JsonResponse({'error': 'Invalid request'})


def calculate_score(missing_skills, improvements, good_points):
    score = 100

    score -= len(missing_skills) * 7
    score -= len(improvements) * 3
    score += len(good_points) * 2

    return max(0, min(score, 100))

