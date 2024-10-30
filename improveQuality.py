from google_images_search import GoogleImagesSearch
import os

# إدخال Google API Key و Custom Search Engine ID
api_key = 'YOUR_API_KEY'  # استبدل 'YOUR_API_KEY' بمفتاح API الخاص بك
cse_id = 'YOUR_CSE_ID'  # استبدل 'YOUR_CSE_ID' بـ CSE ID الخاص بك

# إعداد Google Images Search
gis = GoogleImagesSearch(api_key, cse_id)

# مسار الفولدر الذي يحتوي على الصور
folder_path = 'images'  # قم بتغيير 'images' إلى مسار مجلد الصور

# البحث عن صورة جديدة وتنزيلها
def download_better_image(query, old_image_path):
    try:
        # إعدادات البحث
        search_params = {
            'q': query,
            'num': 1,  # الحصول على نتيجة واحدة فقط
            'fileType': 'jpg|png',
            'safe': 'high',
            'imgType': 'photo',
            'imgSize': 'large',  # الحصول على صورة بجودة عالية
        }

        # تنفيذ البحث
        gis.search(search_params)
        # إذا وجدت نتائج، قم بتنزيل أول صورة
        if gis.results():
            new_image_path = old_image_path  # نفس اسم الصورة القديمة

            # حذف الصورة القديمة
            os.remove(old_image_path)

            # تنزيل الصورة الجديدة
            for image in gis.results():
                image.download(new_image_path)
                break  # نحتاج فقط إلى الصورة الأولى
            print(f"تم استبدال الصورة: {old_image_path}")
        else:
            print(f"لم يتم العثور على نتائج ل: {query}")
    except Exception as e:
        print(f"حدث خطأ أثناء تنزيل الصورة: {e}")

# التحقق من وجود المجلد ومعالجة كل صورة داخله
if os.path.exists(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)

            # استخدام اسم الصورة ككلمة بحث (يمكنك تعديل ذلك ليكون نصًا مختلفًا)
            image_name = os.path.splitext(filename)[0]  # استخراج الاسم بدون الامتداد
            download_better_image(image_name, file_path)
    print("تم استبدال الصور ذات الجودة المنخفضة بصور بجودة عالية.")
else:
    print(f"المجلد '{folder_path}' غير موجود.")
