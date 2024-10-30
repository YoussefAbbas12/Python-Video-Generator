import requests
from bs4 import BeautifulSoup
from docx import Document

# تحديد رابط الأخبار باللغة العربية من موقع BBC
url = 'https://www.bbc.com/arabic'

# جلب محتوى الصفحة باستخدام requests
response = requests.get(url)
if response.status_code == 200:  # التحقق من أن الجلب تم بنجاح
    page_content = response.text

    # تحليل الصفحة باستخدام BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # البحث عن العناوين الرئيسية للأخبار
    # استخدام البحث في العناصر h3 و a مع فحص الفئة (class) لضمان أنها تحتوي على كلمة 'bbc'
    headlines = soup.find_all(['h3', 'a'], class_=lambda value: value and 'bbc' in value)

    # قائمة لتخزين العناوين الفريدة
    news_headlines = []

    # كلمات مفتاحية نستبعدها من العناوين
    excluded_phrases = ["الصفحة الحالية", "رئيسية", "أقسام", "مزيد من الأخبار", "عن الموقع", "الاتصال بنا"]

    # استخراج النصوص والتخلص من التكرارات وتصفية العناوين الغير صالحة
    for headline in headlines:
        text = headline.get_text().strip()
        # التحقق من أن النص طويل بما يكفي، غير مكرر، ولا يحتوي على عبارات مستثناة
        if (len(text) > 20 and 
            text not in news_headlines and 
            not any(excluded in text for excluded in excluded_phrases)):
            news_headlines.append(text)

    # طباعة العناوين للتحقق
    print(f"عدد العناوين المستخرجة بعد التخلص من التكرارات: {len(news_headlines)}")
    for index, headline in enumerate(news_headlines):
        print(f"العنوان {index + 1}: {headline}")

    # التحقق من وجود العناوين
    if len(news_headlines) == 0:
        print("لم يتم استخراج أي عناوين. تأكد من الفئة (class) الخاصة بالعناوين في الصفحة.")
    else:
        # إنشاء مستند Word جديد
        doc = Document()

        # إضافة أول خمس عناوين إلى المستند
        for index, headline in enumerate(news_headlines[:5]):
            doc.add_paragraph(headline)  # إضافة نص العنوان

        # حفظ المستند باسم 'bbc_arabic_news.docx'
        doc_name = 'bbc_arabic_news.docx'
        doc.save(doc_name)
        print(f"تم حفظ الأخبار في ملف {doc_name}")
else:
    print("فشل في جلب الصفحة، تحقق من الرابط.")
