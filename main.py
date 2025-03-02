# app.py
from flask import Flask, render_template, request
import google.generativeai as genai
import textwrap
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

def format_prompt(question):
    return textwrap.dedent(f"""
    <تفكير>
    - السؤال: {question}
    - سأبدأ بتحليل متأنٍ للمشكلة من جميع الجوانب الممكنة.
    - سأتحقق من صحة الافتراضات الأساسية وأبحث عن أي مفارقات محتملة.
    - سأستخدم منهجية علمية في التحليل مع مراعاة السياق العربي.
    </تفكير>

    <خطوة>
    1. تحليل المتطلبات الأساسية للسؤال
    <عدد> 19
    </خطوة>

    <تأمل>
    - هل فهمت السؤال بشكل صحيح؟
    - ما هي الثغرات المحتملة في تحليلي الأولي؟
    <مكافأة> 0.7
    </تأمل>

    <تحقق>
    - التحقق الرياضي: تطبيق الحل على معطيات مختلفة
    - التحقق المنطقي: اختبار الاتساق الداخلي للحل
    </تحقق>

    <تأكيد>
    - التأكد من مطابقة الحل لجميع شروط السؤال
    - المراجعة النهائية للأخطاء المحتملة
    </تأكيد>

    <إجابة>
    // المساحة للإجابة النهائية
    </إجابة>

    <تأمل_نهائي>
    - تقييم شمولية الحل وفعاليته
    - مقترحات لتحسين النهج في المستقبل
    <مكافأة_نهائية> 0.85
    </تأمل_نهائي>
    """)

def extract_tag(text, tag_name):
    start_tag = f"<{tag_name}>"
    end_tag = f"</{tag_name}>"
    start = text.find(start_tag) + len(start_tag)
    end = text.find(end_tag)
    return text[start:end].strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        prompt = format_prompt(question)

        try:
            response = model.generate_content(prompt)
            result = {
                'answer': extract_tag(response.text, 'إجابة'),
                'thinking': extract_tag(response.text, 'تفكير'),
                'verification': extract_tag(response.text, 'تحقق'),
                'final_reflection': extract_tag(response.text, 'تأمل_نهائي')
            }
            return render_template('result.html', question=question, result=result)

        except Exception as e:
            error = f"Error: {str(e)}"
            return render_template('index.html', error=error)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)