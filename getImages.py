from docx import Document
import requests
import os
from bs4 import BeautifulSoup
import re
from PIL import Image
from io import BytesIO

# دالة لقراءة العناوين من ملف Word
def read_news_from_word(file_path):
    doc = Document(file_path)
    headlines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text and not text.startswith("الخبر") and "أحدث الأخبار من BBC Arabic" not in text:
            headlines.append(text)
    return headlines

# دالة لجلب الصور بناءً على عنوان الخبر
def download_images(headlines):
    if not os.path.exists("images"):
        os.makedirs("images")

    index = 1
    for title in headlines:
        # تنظيف عنوان الخبر ليكون صالحاً كاسم ملف
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)
        query = f"{title} site:bbc.com"  # البحث عن الصور باستخدام عنوان الخبر
        url = f"https://www.bing.com/images/search?q={query}"
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # العثور على الصور في نتائج البحث
        images = soup.find_all("img", class_="mimg")  # تحقق من الفئة الصحيحة للصور
        if images:
            img_url = images[0]['src']  # الحصول على عنوان الصورة الأولى
            img_data = requests.get(img_url).content
            
            # استخدام Pillow لتحميل الصورة
            image = Image.open(BytesIO(img_data))

            # تغيير حجم الصورة
            image = image.resize((800, 600))  # تغيير الحجم إلى 800x600 بكسل
            
            # حفظ الصورة
            image.save(f"images/{index}.jpg")
            print(f"تم تحميل صورة لعنوان: {title}")
            index = index + 1
        else:
            print(f"لم يتم العثور على صور لعنوان: {title}")

# المسار إلى ملف Word
word_file_path = 'bbc_arabic_news.docx'

# قراءة العناوين من ملف Word
news_headlines = read_news_from_word(word_file_path)

# تنزيل الصور
download_images(news_headlines)
