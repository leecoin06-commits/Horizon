# Horizon — الرادار المالي العربي

يعمل على GitHub Actions يوميًا عند **12:00 UTC = 15:00 بتوقيت الرياض** (قد تتأخر بداية المهمة عن الموعد).

## التخصيص
- البيتكوين **BTC**، وصندوق **IBIT**، والاقتصاد والأسهم الأمريكية، والحوسبة الكمومية وأثرها على أمن البيتكوين.
- جمع الأخبار عبر RSS وإصدارات Bitcoin Core؛ لا يحتاج إلى مفتاح X.
- التلخيص ثم الترجمة إلى العربية وإنشاء صفحات HTML باتجاه RTL.
- الإعداد المنفصل: `data/config.arabic.json`، فلا يتغير ملف إعداد Horizon الرسمي `data/config.github.json`.
- سير العمل: `.github/workflows/horizon-arabic-daily.yml`، ولا يستبدل سير عمل نشر وثائق Horizon الأصلي.

## الخطوات المطلوبة لتفعيل التشغيل
1. في المستودع افتح **Settings → Secrets and variables → Actions → New repository secret**، وأنشئ السر `OPENAI_API_KEY` بقيمة مفتاح API صالح ومفعل الفوترة. **لا ترسل المفتاح في المحادثة ولا تضعه داخل الكود.**
2. من **Actions** فعّل سير العمل إذا ظهر معطّلًا بعد عملية Fork، ثم افتح **Horizon Arabic Daily Radar → Run workflow** للاختبار.
3. راجع سجل التنفيذ. إذا ظهرت رسالة missing key، تأكد من إضافة السر وصحة الاسم. إذا فشل استدعاء OpenAI فتحقق من الرصيد والصلاحيات والنموذج.
4. تأكد من أن **Settings → Actions → General → Workflow permissions** تسمح بالكتابة، لأن النشر إلى فرع `gh-pages` يحتاج صلاحية كتابة المحتويات.
5. بعد إنشاء فرع `gh-pages`، اختر **Settings → Pages → Build and deployment → Deploy from a branch → gh-pages / (root)**.

## الروابط
- [سير العمل](https://github.com/leecoin06-commits/Horizon/actions/workflows/horizon-arabic-daily.yml)
- [التقرير العربي بعد أول نشر ناجح](https://leecoin06-commits.github.io/Horizon/arabic/)

**مهم:** ملفات التثبيت أصبحت موجودة في GitHub، لكن نجاح التقرير والنشر لم يُتحقق منه حتى الآن؛ إضافة السر وتفعيل Pages وإجراء الاختبار خطوات لازمة. اشتراك ChatGPT لا يغطي رسوم OpenAI API. موقع Pages عام ولا يُناسب بيانات شخصية أو سرية.
