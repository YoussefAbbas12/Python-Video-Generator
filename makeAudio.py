import os
import requests
from docx import Document

# مسار ملف الـ docx
docx_file = "bbc_arabic_news.docx"

# إنشاء دالة لقراءة النص من ملف docx وإرجاع قائمة من الأسطر
def read_docx_lines(file_path):
    doc = Document(file_path)
    lines = [para.text for para in doc.paragraphs if para.text.strip()]  # اجمع الفقرات التي تحتوي على نص فقط
    return lines

# إعداد المتغيرات الخاصة بواجهة API
CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/ErXwobaYiN019PkySvjV"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "sk_4131e611ca5c285a52eabc10e39d608206b68734e18b2100"  # استبدل بمفتاح الـ API الخاص بك
}

# قراءة الأسطر من ملف docx
lines_from_docx = read_docx_lines(docx_file)

# إنشاء مجلد لحفظ الملفات الصوتية إذا لم يكن موجودًا
output_folder = "news_audio"
os.makedirs(output_folder, exist_ok=True)

# تحويل كل سطر إلى ملف صوتي مستقل وحفظه في المجلد المحدد
for i, line in enumerate(lines_from_docx):
    if line.strip():  # التأكد من أن السطر ليس فارغًا
        # إعداد البيانات المرسلة إلى API
        data = {
            "text": line,
            "model_id": "eleven_multilingual_v2",  # استخدم النموذج متعدد اللغات لدعم اللغة العربية
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        # إرسال الطلب إلى API
        response = requests.post(url, json=data, headers=headers)

        # حفظ الملف الصوتي الناتج داخل المجلد news_audio
        audio_filename = os.path.join(output_folder, f"line_{i+1}.mp3")
        with open(audio_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        print(f"Voice for line {i+1} generated and saved as {audio_filename}")
