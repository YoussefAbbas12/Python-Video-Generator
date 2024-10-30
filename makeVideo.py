import os
from docx import Document
from moviepy.editor import *

# إعدادات المسارات
image_folder = "images"  # مجلد الصور
audio_folder = "news_audio"  # مجلد الصوت
word_file = "bbc_arabic_news.docx"  # ملف الوورد

# تحميل محتويات ملف الوورد
document = Document(word_file)
news_texts = [para.text.strip() for para in document.paragraphs if para.text.strip()]

# الحصول على جميع الصور في المجلد
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
print(f"الصور المتاحة: {image_files}")  # طباعة أسماء الصور المتاحة

# إنشاء الفيديو
clips = []

# إضافة كل خبر إلى الفيديو
for idx, news in enumerate(news_texts):
    # تأكد من وجود صورة في المجلد
    if idx < len(image_files):
        image_path = os.path.join(image_folder, image_files[idx])  # احصل على مسار الصورة
        print(f"تحميل الصورة: {image_path}")  # طباعة اسم الصورة المحملة
    else:
        print(f"لا توجد صورة متاحة للخبر: {news}")
        continue  # الانتقال إلى الخبر التالي إذا لم تكن هناك صورة

    # تحميل الصورة كـ Clip
    img_clip = ImageClip(image_path).set_duration(5).set_position('center').resize(height=480)

    # إضافة ملف الصوت
    audio_file = os.path.join(audio_folder, f"line_{idx + 1}.mp3")
    if os.path.exists(audio_file):
        audio = AudioFileClip(audio_file)
        img_clip = img_clip.set_audio(audio).set_duration(audio.duration)
    else:
        print(f"لا يوجد ملف صوتي للخبر: {news}")  # طباعة رسالة إذا لم يكن هناك ملف صوتي

    clips.append(img_clip)

# دمج جميع المقاطع
final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile("output_video.mp4", fps=24)

print("تم إنشاء الفيديو بنجاح!")
