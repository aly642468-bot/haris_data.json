# -*- coding: utf-8 -*-
# بوت حارس (النسخة 3): تعليم بايثون والأمن السيبراني الدفاعي
# يعمل بدون مكتبات خارجية (مكتبات بايثون الجاهزة فقط)

import datetime
import json
import os
import random
import re
import secrets
import string
import time
import traceback
import urllib.error
import urllib.request

# ==================== الإعدادات ====================
TOKEN = "9005576115:AAHNA1NCIlSLN2UD8i4FjHTw6ZDCgxrnF84"
GEMINI_KEY = ""  # ضع مفتاح Gemini هنا بين علامتي التنصيص (اختياري)
GEMINI_MODELS = ["gemini-3.5-flash", "gemini-3-flash-preview",
                 "gemini-2.5-flash"]
MAX_AI_PER_DAY = 30  # أقصى عدد أسئلة Gemini لكل مستخدم في اليوم
DEV_USERNAME = "ix_120"  # يوزر المطور (بدون @)

URL = "https://api.telegram.org/bot" + TOKEN

# ==================== المحتوى ====================
TIPS = [
    "فعّل التحقق بخطوتين (2FA) في كل حساباتك المهمة.",
    "لا تستخدم نفس كلمة السر في أكثر من موقع.",
    "لا تضغط على روابط مشبوهة حتى لو جاتك من صديق.",
    "حدّث جوالك وتطبيقاتك دايماً، التحديثات تسد الثغرات.",
    "كلمة السر الطويلة أقوى من القصيرة المعقدة.",
    "لا تدخل حساباتك المهمة من واي فاي عام بدون حماية.",
    "نزّل التطبيقات من المتاجر الرسمية فقط.",
    "لا تعطي كود التحقق (OTP) لأي أحد حتى لو ادّعى إنه من البنك.",
    "خذ نسخة احتياطية من ملفاتك المهمة بشكل دوري.",
    "إذا العرض كأنه حلم (جائزة، ربح سريع)، غالباً هو احتيال.",
]

LESSONS = [
    ("1. المتغيرات",
     "المتغير علبة تحط فيها قيمة وتعطيها اسم:\n\n"
     "name = \"بدر\"\nage = 20\nprint(name)\nprint(age)\n\n"
     "النص بين تنصيص، والرقم بدون تنصيص."),
    ("2. أنواع البيانات",
     "أشهر الأنواع:\n"
     "str = نص\nint = رقم صحيح\nfloat = رقم عشري\nbool = صح أو خطأ\n\n"
     "x = 3.14\nprint(type(x))\n\n"
     "الدالة type تقولك نوع القيمة."),
    ("3. العمليات الحسابية",
     "+  جمع\n-  طرح\n*  ضرب\n/  قسمة\n//  قسمة بدون كسور\n"
     "%  باقي القسمة\n**  أُس\n\n"
     "print(10 % 3)   # يطبع 1\nprint(2 ** 3)   # يطبع 8"),
    ("4. الشروط if",
     "الشرط يخلي البرنامج يقرر:\n\n"
     "age = 20\nif age >= 18:\n    print(\"بالغ\")\nelse:\n    print(\"قاصر\")\n\n"
     "انتبه للمسافات (4 مسافات) تحت if و else."),
    ("5. الحلقات",
     "حلقة for تكرر عدد معين:\n\n"
     "for i in range(5):\n    print(i)\n\n"
     "حلقة while تكرر ما دام الشرط صح:\n\n"
     "n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1"),
    ("6. القوائم",
     "القائمة تحفظ عدة قيم:\n\n"
     "fruits = [\"تمر\", \"عنب\"]\nprint(fruits[0])   # الأول\n"
     "fruits.append(\"موز\")   # إضافة\nprint(len(fruits))   # العدد\n\n"
     "الترقيم يبدأ من 0 مو من 1."),
    ("7. الدوال",
     "الدالة كود جاهز تستدعيه وقت ما تبي:\n\n"
     "def hello(name):\n    print(\"هلا\", name)\n\n"
     "hello(\"بدر\")\n\n"
     "الكلمة def تعرّف الدالة."),
    ("8. القواميس",
     "القاموس يخزّن قيمة مقابل مفتاح:\n\n"
     "user = {\"name\": \"بدر\", \"age\": 20}\n"
     "print(user[\"name\"])\nuser[\"city\"] = \"الرياض\""),
    ("9. التعامل مع الأخطاء",
     "try/except يمنع البرنامج من الانهيار:\n\n"
     "try:\n    x = int(\"abc\")\nexcept ValueError:\n    print(\"هذا مو رقم\")\n\n"
     "البوت حقك يستخدم نفس الفكرة عشان ما يوقف."),
    ("10. GitHub: ما هو ولماذا",
     "GitHub موقع يحفظ مشاريعك ونسخها القديمة، ويعرض أعمالك للناس.\n\n"
     "مفاهيم أساسية:\n"
     "Repository = مجلد مشروعك على الموقع\n"
     "Commit = حفظ نقطة في تاريخ المشروع\n"
     "Push = رفع تعديلاتك للموقع\n"
     "Branch = نسخة موازية تجرّب فيها بأمان\n\n"
     "قبل ما تبدأ:\n"
     "1) سوّ حساب بكلمة سر قوية\n"
     "2) فعّل التحقق بخطوتين\n"
     "3) لا ترفع أبداً توكن البوت ولا مفاتيح الذكاء الاصطناعي"),
    ("11. أوامر Git الأساسية",
     "git init   (يبدأ مشروع جديد)\n"
     "git add .   (يجهّز الملفات)\n"
     "git commit -m \"first version\"   (يحفظ نسخة)\n"
     "git push   (يرفع للموقع)\n\n"
     "ملف .gitignore: اكتب فيه أسماء الملفات اللي ما تبي ترفعها، مثل config.py\n\n"
     "لو رفعت سر بالغلط: ألغِه من مصدره وسوّ غيره. حذف الملف ما يكفي "
     "لأنه يبقى في سجل التعديلات."),
]

QUIZ = [
    ("وش يطبع print(2 + 3)؟", ["23", "5", "خطأ"], 1),
    ("أي كلمة سر أقوى؟", ["12345678", "ahmed2000", "Tr#9vK!mQ2xL"], 2),
    ("وش هو التصيّد (Phishing)؟",
     ["رسالة مزورة تسرق بياناتك", "نوع فيروس للجهاز", "برنامج حماية"], 0),
    ("أي رمز يخزّن قيمة في متغير؟", ["==", "=", "!="], 1),
    ("وش فايدة التحقق بخطوتين؟",
     ["ما تفيد", "تحمي حسابك حتى لو انسرقت كلمة السر", "للشركات فقط"], 1),
    ("وش نوع القيمة 3.14؟", ["int", "float", "str"], 1),
    ("وش ناتج 10 % 3؟", ["1", "3", "0"], 0),
    ("بأي كلمة نعرّف دالة في بايثون؟", ["func", "def", "fun"], 1),
    ("فيروس الفدية (Ransomware) وش يسوي؟",
     ["يقفل ملفاتك ويطلب فلوس", "يسرّع الجوال", "ينظّف الجهاز"], 0),
    ("وش الأنسب للواي فاي العام؟",
     ["أدخل حساباتي عادي", "أستخدم VPN وأتجنب الحسابات المهمة",
      "أعطي كلمة السر لأي أحد"], 1),
    ("وش ناتج len([1, 2, 3])؟", ["2", "3", "4"], 1),
    ("الرابط اللي يبدأ بـ https يعني؟",
     ["الاتصال مشفّر لكن الموقع ممكن يكون مزوّر",
      "الموقع مضمون 100%", "الموقع بدون تشفير"], 0),
    ("أنسب طريقة لحفظ كلمات السر؟",
     ["رسالة لنفسي في الواتساب", "مدير كلمات سر موثوق", "نفس الكلمة للكل"], 1),
    ("وش يسوي الأمر git push؟",
     ["يرفع تعديلاتك للموقع", "يحذف المشروع", "يغيّر كلمة السر"], 0),
    ("رفعت توكن على GitHub بالغلط، وش تسوي؟",
     ["أحذف الملف وخلاص", "ألغي التوكن وأسوّي غيره", "أتجاهل الموضوع"], 1),
]

GLOSSARY = [
    ("التصيّد Phishing",
     "رسائل أو مواقع مزورة تتنكر بشكل جهة موثوقة عشان تسرق بياناتك."),
    ("البرمجيات الخبيثة Malware",
     "أي برنامج يضر جهازك أو يسرق بياناتك، مثل الفيروسات وأحصنة طروادة."),
    ("جدار الحماية Firewall",
     "حاجز يراقب الاتصالات الداخلة والخارجة ويمنع المشبوه منها."),
    ("VPN",
     "يشفّر اتصالك ويخفي عنوانك الحقيقي، مفيد في الشبكات العامة."),
    ("التشفير Encryption",
     "تحويل البيانات لشكل غير مقروء إلا لمن عنده المفتاح."),
    ("الفدية Ransomware",
     "برنامج يقفل ملفاتك ويطلب مبلغ لفكها. الحماية: نسخ احتياطية وتحديثات."),
    ("الهندسة الاجتماعية",
     "خداع الناس نفسياً عشان يعطون معلومات أو يضغطون روابط، بدل اختراق الأجهزة."),
    ("هجوم DDoS",
     "إغراق موقع بطلبات كثيرة جداً عشان يتعطل."),
    ("الهاش Hash",
     "بصمة رقمية ثابتة للبيانات، والمواقع تخزّن بها كلمات السر بدل النص الصريح."),
    ("التحقق بخطوتين 2FA",
     "طبقة حماية ثانية بعد كلمة السر، مثل كود يوصلك على الجوال."),
]

ROADMAP = (
    "🗺️ خارطة الطريق المقترحة:\n\n"
    "1) أساسيات بايثون: متغيرات، شروط، حلقات، قوائم، دوال (شهر إلى شهرين)\n"
    "2) مشاريع صغيرة: حاسبة، لعبة تخمين، بوت تيليجرام\n"
    "3) أساسيات الشبكات: IP، DNS، المنافذ، HTTP\n"
    "4) أساسيات الأمن: كلمات السر، التشفير، التصيّد، الحماية\n"
    "5) تدرّب قانونياً: مختبرات تعليمية مرخّصة وأجهزتك الشخصية فقط\n"
    "6) اكتب أدوات دفاعية بسيطة بنفسك (فاحص روابط، مولّد كلمات سر)\n\n"
    "القاعدة الذهبية: التدريب فقط على أجهزة وأنظمة تملكها أو معك إذن مكتوب."
)

# ---------- الإنجليزية ----------
EN_WORDS = [
    ("error", "خطأ", "I got an error."),
    ("warning", "تحذير", "This is a warning."),
    ("file", "ملف", "Open the file."),
    ("folder", "مجلد", "Create a new folder."),
    ("install", "يثبّت", "Install Python first."),
    ("update", "يحدّث / تحديث", "Update your phone."),
    ("password", "كلمة السر", "Use a strong password."),
    ("username", "اسم المستخدم", "Enter your username."),
    ("token", "رمز وصول (توكن)", "Never share your token."),
    ("key", "مفتاح", "Keep your key secret."),
    ("secret", "سر", "This is a secret."),
    ("permission", "إذن / صلاحية", "The app needs permission."),
    ("denied", "مرفوض", "Permission denied."),
    ("not found", "غير موجود", "File not found."),
    ("missing", "ناقص / مفقود", "A file is missing."),
    ("invalid", "غير صالح", "Invalid password."),
    ("failed", "فشل", "The login failed."),
    ("success", "نجاح", "Upload success."),
    ("connection", "اتصال", "No internet connection."),
    ("timeout", "انتهت المهلة", "The request timed out."),
    ("server", "خادم (سيرفر)", "The server is down."),
    ("request", "طلب", "Send a request."),
    ("response", "رد / استجابة", "Wait for the response."),
    ("package", "حزمة (مكتبة)", "Install the package."),
    ("module", "وحدة (مكتبة بايثون)", "Import the module."),
    ("function", "دالة", "Call the function."),
    ("variable", "متغير", "Create a variable."),
    ("string", "نص", "A string is text."),
    ("list", "قائمة", "Add an item to the list."),
    ("loop", "حلقة تكرار", "Use a loop."),
    ("condition", "شرط", "Check the condition."),
    ("syntax", "قواعد كتابة الكود", "It is a syntax error."),
    ("exception", "استثناء (خطأ أثناء التشغيل)", "An exception occurred."),
    ("crash", "انهيار / توقف مفاجئ", "The app crashed."),
    ("bug", "علّة برمجية", "Fix the bug."),
    ("fix", "يصلّح", "Fix the error."),
    ("run", "يشغّل", "Run the script."),
    ("save", "يحفظ", "Save the file."),
    ("delete", "يحذف", "Delete the message."),
    ("download", "تنزيل", "Download the file."),
    ("upload", "رفع", "Upload your project."),
    ("network", "شبكة", "Connect to the network."),
    ("link", "رابط", "Do not click the link."),
    ("login", "تسجيل الدخول", "Login to your account."),
    ("account", "حساب", "Create an account."),
    ("security", "أمن / حماية", "Security is important."),
    ("threat", "تهديد", "Report the threat."),
    ("protect", "يحمي", "Protect your data."),
    ("encrypt", "يشفّر", "Encrypt the file."),
    ("hash", "بصمة رقمية", "Store the hash."),
    ("attack", "هجوم", "Prevent the attack."),
    ("scam", "نصب / احتيال", "This is a scam."),
    ("backup", "نسخة احتياطية", "Make a backup."),
]

ERROR_HINTS = {
    "permission denied": "الإذن مرفوض: ما عندك صلاحية على الملف، أو التطبيق ما أخذ إذن.",
    "command not found": "الأمر غير موجود: غالباً غير مثبّت أو مكتوب غلط. جرّب pkg install اسم_الأداة.",
    "no such file or directory": "لا يوجد ملف أو مجلد بهذا الاسم: تأكد من الاسم والمسار.",
    "syntaxerror": "خطأ في كتابة الكود: قوس أو تنصيص أو نقطتين ناقصة، أو كلمة مكتوبة غلط.",
    "unexpected eof": "الملف انتهى قبل ما يكتمل الكود: غالباً قوس أو تنصيص أو بلوك ناقص في آخر الملف.",
    "indentationerror": "خطأ في المسافات: بايثون يحتاج 4 مسافات منتظمة داخل if و for و def.",
    "nameerror": "اسم غير معرّف: استخدمت متغيراً أو دالة قبل ما تعرّفها، أو كتبت اسمها غلط.",
    "typeerror": "نوع القيمة غير مناسب للعملية: مثل جمع نص مع رقم.",
    "valueerror": "قيمة غير صالحة: مثل int(\"abc\").",
    "keyerror": "المفتاح غير موجود في القاموس.",
    "indexerror": "رقم خارج حدود القائمة: تذكّر أن الترقيم يبدأ من 0.",
    "modulenotfounderror": "المكتبة غير مثبّتة: ثبّتها بـ pip install اسم_المكتبة.",
    "importerror": "تعذّر استيراد المكتبة أو الدالة: تأكد من الاسم والتثبيت.",
    "connection refused": "الاتصال مرفوض: الخادم مغلق، أو العنوان أو المنفذ غلط.",
    "timed out": "انتهت مهلة الاتصال: الإنترنت ضعيف أو الخادم ما يرد.",
    "unauthorized": "غير مصرّح: التوكن أو المفتاح غلط أو منتهي.",
    "forbidden": "ممنوع: ما عندك صلاحية للوصول.",
    "conflict": "تعارض (خطأ 409): غالباً نسختين من البوت تشتغل بنفس التوكن، أوقف وحدة.",
    "zerodivisionerror": "قسمة على صفر.",
    "attributeerror": "الشيء ما عنده هذه الخاصية أو الدالة.",
}

# ---------- الشروحات والقنوات ----------
RESOURCES = {
    "res_py": ("🐍 بايثون", [
        "• راكوان للبرمجة (CodeRK): https://www.youtube.com/@Rakwan",
        "• Elzero Web School (أسامة الزيرو): https://www.elzero.org",
        "• Codezilla: ابحث عنه في يوتيوب بهذا الاسم",
        "• Coder Shiyar: https://github.com/codershiyar/python",
        "• أكاديمية حسوب: https://academy.hsoub.com",
    ]),
    "res_cy": ("🛡️ الأمن السيبراني", [
        "• كورس أمن سيبراني (Coder Shiyar): https://github.com/codershiyar/cybersecurity",
        "• Boot2Root: ابحث عنها في يوتيوب بهذا الاسم",
    ]),
    "res_tx": ("📱 Termux", [
        "• التوثيق الرسمي: https://wiki.termux.com و https://termux.dev/en/",
        "• شروحات السوري: https://www.youtube.com/@alswry00\n"
        "  ⚠️ خذ منها Termux وبايثون فقط. تجنّب أقسام «تفعيل الأرقام الأجنبية» "
        "و«فك الحظر» و«الصيد» والثغرات الهجومية، فقد تخالف القانون وسياسات المنصات.",
    ]),
    "res_en": ("🇬🇧 الإنجليزية", [
        "• zAmericanEnglish (من الصفر حتى الطلاقة): https://www.youtube.com/@ZAmericanEnglish",
        "• قناة freeCodeCamp على يوتيوب (فعّل الترجمة التلقائية)",
    ]),
}
RESOURCES_NOTE = ("\n\nقبل ما تتابع أي قناة: تأكد إنها تعلّم الحماية والفهم، "
                  "لا اختراق حسابات الناس. القنوات اللي تعد بـ «تهكير» "
                  "غالباً مخالفة للقانون أو خدعة تصيب جوالك.")

# ---------- مكافآت النجوم (روابط إحالة) ----------
REWARD_LINKS = [
    ("🥇 رابط المكافآت الأول", "http://t.me/StarsovComBot?start=MA40ERkpL"),
    ("⛏️ رابط التعدين الثاني", "http://t.me/StarsovEarnBot?start=9sXzRc5r0"),
    ("🎁 رابط المكافآت الثالث", "http://t.me/StarsMakeBot?start=46bOOP1q4"),
    ("🎮 رابط الألعاب الرابع", "http://t.me/StarsovGamesBot?start=2500yV0dX"),
]
REWARDS_TEXT = (
    "⭐ مكافآت النجوم\n\n"
    "لو ما عندك نجوم، تقدر تجرّب هذي التطبيقات، ولكل واحد منها شروطه.\n\n"
    "⚠️ إفصاح مهم:\n"
    "• هذي روابط إحالة لصاحب البوت (بدر)، وله عمولة لو انضميت.\n"
    "• الأرباح غير مضمونة، وشروط كل تطبيق عليه.\n"
    "• لا تعطي أي تطبيق كلمة سرك أو كود التحقق أو بياناتك الحساسة.\n"
    "• لا تدفع مقابل وعود الربح السريع.\n\n"
    "💡 بديل مجاني داخل البوت: اكسب نقاط XP من التعلم والتحديات."
)

# ---------- أدوات الأمن ----------
SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "cutt.ly", "is.gd"]
PHISH_WORDS = ["login", "verify", "update", "secure", "account",
               "bank", "gift", "free", "prize", "password"]

SECRET_PATTERNS = [
    ("توكن بوت تيليجرام", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    ("مفتاح Anthropic", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("مفتاح يشبه OpenAI", r"sk-[A-Za-z0-9]{32,}"),
    ("توكن GitHub", r"gh[pousr]_[A-Za-z0-9]{36,}"),
    ("توكن GitHub", r"github_pat_[A-Za-z0-9_]{50,}"),
    ("مفتاح Google / Gemini", r"AIza[0-9A-Za-z_-]{35}"),
    ("مفتاح Google / Gemini", r"\bAQ\.[A-Za-z0-9_-]{30,}"),
    ("مفتاح AWS", r"AKIA[0-9A-Z]{16}"),
    ("كلمة سر مكتوبة في الكود",
     r"(?i)(password|passwd|pwd|secret|token|api_key|apikey)\s*[=:]\s*[\"'][^\"']{6,}[\"']"),
]
PLACEHOLDERS = ("ضع_", "your", "here", "xxx", "example")

GITHUB_INTRO = (
    "🐙 GitHub يحفظ مشاريعك ويعلّمك طريقة عمل الفرق.\n\n"
    "ابدأ بالدرسين، وقبل ما ترفع أي كود، افحصه بفاحص الأسرار "
    "عشان ما ترفع توكن أو مفتاح بالغلط."
)

# ---------- تعليمات Gemini ----------
TUTOR_RULES = (
    "أنت مدرّب ودود داخل بوت «حارس» لتعليم بايثون والأمن السيبراني الدفاعي "
    "للمبتدئين، بلهجة خليجية بسيطة. الطالب يستخدم جواله فقط ولا يعرف "
    "إنجليزي، فاشرح أي مصطلح إنجليزي بالعربي. "
    "ساعد في الحماية والتوعية والتعلّم القانوني فقط (أجهزتك الخاصة ومختبرات "
    "مرخّصة). ارفض بلطف أي طلب لاختراق حسابات أو أجهزة الآخرين أو كتابة "
    "برمجيات خبيثة، واقترح بديلاً تعليمياً قانونياً. "
    "إذا أرسل الطالب كوداً أو خطأً: اشرح الخطأ ببساطة، ثم أعطه تلميحاً "
    "ولا تعطِ الحل كاملاً من أول مرة، واطلب منه المحاولة. إذا طلب الحل أو "
    "فشل مرتين، أعطه الحل مع شرح سطراً بسطر ثم سؤالاً قصيراً للتأكد من فهمه."
)
ASK_SYSTEM = TUTOR_RULES
REVIEW_SYSTEM = (
    TUTOR_RULES + " مهمتك الآن مراجعة كود بايثون أو شرح رسالة خطأ، "
    "ولا تكتب كلاماً زائداً."
)
DETAIL_LEVELS = ["short", "normal", "deep"]
DETAIL_LABELS = {"short": "مختصر", "normal": "مفصّل", "deep": "تفصيل ممل"}
DETAIL_PROMPTS = {
    "short": "اجعل الجواب مختصراً جداً (أقل من 80 كلمة).",
    "normal": "اجعل الجواب واضحاً ومفصّلاً بشكل متوسط (حتى 200 كلمة).",
    "deep": ("اشرح بتفصيل ممل وخطوة بخطوة مع تشبيهات وأمثلة متعددة، "
             "وقسّم الشرح لخطوات صغيرة جداً ولا تفترض أي معرفة سابقة."),
}

# ==================== القوائم ====================
def btn(text, data):
    return {"text": text, "callback_data": data}


HOME = btn("🏠 القائمة الرئيسية", "menu")
BACK = [[HOME]]

MAIN_MENU = [
    [btn("📚 التعلّم", "m_learn"), btn("🛡️ الأمن", "m_sec")],
    [btn("🤖 Gemini", "m_ai"), btn("🇬🇧 الإنجليزية", "m_en")],
    [btn("🎯 التحديات", "m_play"), btn("🎥 الشروحات", "res")],
    [btn("⭐ مكافآت النجوم", "rewards"), btn("🏆 ملفي", "profile")],
    [btn("👨‍💻 المطور", "dev")],
]

SUBMENUS = {
    "m_learn": ("📚 التعلّم", [
        [btn("📘 دروس بايثون", "lessons"), btn("🐙 GitHub", "github")],
        [btn("🎥 الشروحات والقنوات", "res"), btn("🗺️ خارطة الطريق", "roadmap")],
    ]),
    "m_sec": ("🛡️ الأمن", [
        [btn("🛡️ نصيحة أمنية", "tip"), btn("📖 قاموس الأمن", "glossary")],
        [btn("🔗 فحص رابط", "link"), btn("🔐 فحص كلمة سر", "pw")],
        [btn("🔑 مولّد كلمة سر", "gen"), btn("🔎 فاحص الأسرار", "secrets")],
    ]),
    "m_en": ("🇬🇧 الإنجليزية", [
        [btn("📝 كلمة اليوم", "word"), btn("🧩 اختبار كلمات", "wquiz")],
        [btn("🔤 مترجم الأخطاء", "err"), btn("🎥 قنوات الإنجليزية", "res_en")],
    ]),
    "m_play": ("🎯 التحديات", [
        [btn("🎯 تحدي اليوم", "daily"), btn("🧠 اختبار", "quiz")],
        [btn("🏆 ملفي", "profile")],
    ]),
}

CMDS = {
    "/start": "menu", "/menu": "menu", "/help": "help", "/tip": "tip",
    "/quiz": "quiz", "/gen": "gen", "/lessons": "lessons",
    "/score": "profile", "/profile": "profile", "/daily": "daily",
    "/glossary": "glossary", "/roadmap": "roadmap", "/ask": "ask",
    "/review": "review", "/link": "link", "/check": "pw",
    "/github": "github", "/secrets": "secrets", "/error": "err",
    "/word": "word", "/rewards": "rewards", "/resources": "res",
    "/dev": "dev",
}
BOT_COMMANDS = [
    ("start", "القائمة الرئيسية"), ("daily", "تحدي اليوم"),
    ("profile", "ملفي ومستواي"), ("ask", "اسأل Gemini"),
    ("quiz", "اختبار سريع"), ("word", "كلمة إنجليزية"),
    ("help", "المساعدة"),
]
MODES = ("ask", "review", "link", "pw", "secrets", "err")

# ==================== التقدم والنقاط ====================
try:
    DATA_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "haris_data.json")
except Exception:
    DATA_FILE = "haris_data.json"

LESSON_XP = 10
QUIZ_XP = 10
QUIZ_DAILY_CAP = 50
DAILY_XP = 15

DEFAULTS = {"xp": 0, "streak": 0, "last": "", "lessons": [], "correct": 0,
            "total": 0, "badges": [], "daily": "", "qday": "", "qxp": 0,
            "secrets": False, "wcorrect": 0, "detail": "normal",
            "aiday": "", "aicount": 0}

BADGES = [
    ("first", "📘 أول درس", lambda u: len(u["lessons"]) >= 1),
    ("five", "📚 خمسة دروس", lambda u: len(u["lessons"]) >= 5),
    ("all", "🎓 كل الدروس", lambda u: len(u["lessons"]) >= len(LESSONS)),
    ("ten", "🧠 عشر إجابات صحيحة", lambda u: u["correct"] >= 10),
    ("words", "🇬🇧 عشر كلمات", lambda u: u["wcorrect"] >= 10),
    ("s3", "🔥 ثلاثة أيام متتالية", lambda u: u["streak"] >= 3),
    ("s7", "⚡ أسبوع متتالي", lambda u: u["streak"] >= 7),
    ("scan", "🔎 صائد الأسرار", lambda u: u["secrets"]),
    ("lv5", "🏅 المستوى 5", lambda u: u["xp"] >= 400),
]


def load_data():
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False)
    except Exception as e:
        print("تعذر حفظ التقدم:", e)


users = load_data()
modes = {}
history = {}
last_err = {}


def today_str():
    return datetime.date.today().isoformat()


def get_user(chat):
    u = users.setdefault(str(chat), {})
    for k, v in DEFAULTS.items():
        if k not in u:
            u[k] = list(v) if isinstance(v, list) else v
    return u


def level_of(xp):
    return xp // 100 + 1


def bar_of(xp):
    n = (xp % 100) // 10
    return "▰" * n + "▱" * (10 - n)


def touch(u):
    t = datetime.date.today()
    if u["last"] == t.isoformat():
        return False
    y = (t - datetime.timedelta(days=1)).isoformat()
    u["streak"] = u["streak"] + 1 if u["last"] == y else 1
    u["last"] = t.isoformat()
    return True


def add_xp(chat, amount):
    u = get_user(chat)
    notes = []
    if touch(u):
        amount += 5
        notes.append("📅 +5 XP حضور اليوم (🔥 %d يوم متتالي)" % u["streak"])
    old = level_of(u["xp"])
    u["xp"] += amount
    if level_of(u["xp"]) > old:
        notes.append("🎉 ترقيت للمستوى %d!" % level_of(u["xp"]))
    for bid, title, cond in BADGES:
        if bid not in u["badges"] and cond(u):
            u["badges"].append(bid)
            notes.append("🏅 شارة جديدة: " + title)
    save_data()
    return notes


def award(chat, amount):
    notes = add_xp(chat, amount)
    u = get_user(chat)
    lines = []
    if amount:
        lines.append("⭐ +%d XP" % amount)
    lines += notes
    lines.append("%s  المستوى %d" % (bar_of(u["xp"]), level_of(u["xp"])))
    return "\n".join(lines)


def quiz_gain(u):
    t = today_str()
    if u["qday"] != t:
        u["qday"] = t
        u["qxp"] = 0
    g = max(0, min(QUIZ_XP, QUIZ_DAILY_CAP - u["qxp"]))
    u["qxp"] += g
    return g


def profile_text(chat):
    u = get_user(chat)
    names = [t for bid, t, c in BADGES if bid in u["badges"]]
    if names:
        badges = "\n".join("• " + n for n in names)
    else:
        badges = "ما عندك شارات بعد، كمّل وبتجيك."
    return ("🏆 ملفك\n\nالمستوى: %d\n%s  (%d XP)\n"
            "🔥 أيام متتالية: %d\n"
            "✅ إجابات صحيحة: %d من %d\n"
            "📘 دروس مكتملة: %d من %d\n\nالشارات:\n%s"
            % (level_of(u["xp"]), bar_of(u["xp"]), u["xp"], u["streak"],
               u["correct"], u["total"], len(u["lessons"]), len(LESSONS),
               badges))


# ==================== تيليجرام ====================
def call(method, data=None):
    body = json.dumps(data or {}).encode()
    req = urllib.request.Request(
        URL + "/" + method, body, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def send(chat, text, buttons=None):
    chunks = [text[i:i + 3800] for i in range(0, len(text), 3800)] or [" "]
    for n, chunk in enumerate(chunks):
        data = {"chat_id": chat, "text": chunk,
                "link_preview_options": {"is_disabled": True}}
        if buttons and n == len(chunks) - 1:
            data["reply_markup"] = {"inline_keyboard": buttons}
        call("sendMessage", data)


def delete_message(chat, mid):
    try:
        call("deleteMessage", {"chat_id": chat, "message_id": mid})
        return True
    except Exception:
        return False


# ==================== Gemini ====================
_good_model = []


def gemini_call(model, system, contents):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/%s"
           ":generateContent" % model)
    body = json.dumps({
        "system_instruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.6},
    }).encode()
    req = urllib.request.Request(
        url, body, {"Content-Type": "application/json",
                    "x-goog-api-key": GEMINI_KEY})
    return json.load(urllib.request.urlopen(req, timeout=60))


def gemini_text(data):
    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts if not p.get("thought"))
    except Exception:
        return ""


def ask_ai(chat, text, system):
    if not GEMINI_KEY:
        return ("🤖 Gemini غير مفعّل بعد.\n"
                "ضع مفتاح Gemini في المتغير GEMINI_KEY أعلى الكود.")
    u = get_user(chat)
    if u["aiday"] != today_str():
        u["aiday"] = today_str()
        u["aicount"] = 0
    if u["aicount"] >= MAX_AI_PER_DAY:
        return "وصلت للحد اليومي من أسئلة Gemini، ارجع بكرة."
    u["aicount"] += 1

    system = system + " " + DETAIL_PROMPTS[u["detail"]]
    hist = history.setdefault(chat, [])
    hist.append({"role": "user", "parts": [{"text": text[:3000]}]})
    while len(hist) > 9:
        del hist[:2]

    order = _good_model + [m for m in GEMINI_MODELS if m not in _good_model]
    reply = None
    for model in order:
        try:
            data = gemini_call(model, system, hist)
        except urllib.error.HTTPError as e:
            print("Gemini error:", model, e.code)
            if e.code == 404:
                continue
            hist.pop()
            if e.code in (400, 401, 403):
                return "تعذّر الاتصال بـ Gemini. تأكد من المفتاح (GEMINI_KEY)."
            if e.code == 429:
                return "وصلت حد الاستخدام لدى Gemini، جرّب بعد شوي."
            return "حصل خطأ من Gemini (رمز %d)، جرّب بعد شوي." % e.code
        except Exception as e:
            print("Gemini error:", e)
            hist.pop()
            return "تعذّر الاتصال بـ Gemini، تأكد من الإنترنت وجرّب مرة ثانية."
        answer = gemini_text(data)
        if not answer:
            hist.pop()
            if data.get("promptFeedback", {}).get("blockReason"):
                return "ما قدرت أجاوب على هذا الطلب. جرّب صياغة ثانية."
            return "ما وصلني رد، جرّب مرة ثانية."
        _good_model[:] = [model]
        reply = answer
        break
    if reply is None:
        hist.pop()
        return "ما لقيت نموذج Gemini متاح حالياً، جرّب بعد شوي."
    hist.append({"role": "model", "parts": [{"text": reply}]})
    return reply


# ==================== أدوات الأمن ====================
def strength(p):
    s = 0
    if len(p) >= 12:
        s += 2
    elif len(p) >= 8:
        s += 1
    if any(c.islower() for c in p) and any(c.isupper() for c in p):
        s += 1
    if any(c.isdigit() for c in p):
        s += 1
    if any(c in string.punctuation for c in p):
        s += 1
    return s


def check_password(p):
    labels = ["ضعيفة جداً", "ضعيفة", "ضعيفة", "متوسطة", "جيدة", "قوية"]
    notes = []
    if len(p) < 12:
        notes.append("• خلّها 12 حرف أو أكثر")
    if not (any(c.islower() for c in p) and any(c.isupper() for c in p)):
        notes.append("• اخلط حروف كبيرة وصغيرة")
    if not any(c.isdigit() for c in p):
        notes.append("• أضف أرقام")
    if not any(c in string.punctuation for c in p):
        notes.append("• أضف رموز مثل !@#")
    text = "قوتها: " + labels[strength(p)]
    if notes:
        text += "\n\nلتحسينها:\n" + "\n".join(notes)
    text += "\n\n⚠️ استخدم كلمات تجريبية فقط، لا تكتب كلمة سرك الحقيقية أبداً."
    return text


def check_link(url):
    u = url.strip().lower()
    host = u.split("//")[-1].split("/")[0]
    problems = []
    if u.startswith("http://"):
        problems.append("الرابط بدون تشفير (http)")
    if "@" in host:
        problems.append("فيه علامة @ داخل العنوان (خدعة معروفة)")
    if host.replace(".", "").replace(":", "").isdigit():
        problems.append("عنوان رقمي (IP) بدل اسم موقع")
    if host.startswith("xn--") or ".xn--" in host:
        problems.append("أحرف مموِّهة في اسم الموقع (قد تقلّد موقعاً معروفاً)")
    if host.count("-") >= 3:
        problems.append("اسم الموقع فيه شرطات كثيرة")
    if host.count(".") >= 4:
        problems.append("نطاقات فرعية كثيرة (ممكن تمويه)")
    if host in SHORTENERS:
        problems.append("رابط مختصر يخفي الوجهة الحقيقية")
    if re.search(r"\.(apk|exe|scr)(\?|$|/)", u):
        problems.append("الرابط يحمّل ملف تنفيذي (apk / exe)")
    found = [w for w in PHISH_WORDS if w in u]
    if found:
        problems.append("كلمات شائعة في التصيّد: " + ", ".join(found[:3]))
    if not problems:
        return ("ما لقيت علامات واضحة.\n"
                "لكن هذا فحص بسيط ولا يضمن السلامة، "
                "لا تدخل بياناتك إلا إذا كنت متأكد من الموقع.")
    return ("⚠️ علامات مشبوهة:\n\n" + "\n".join("• " + p for p in problems) +
            "\n\nلا تضغط عليه ولا تدخل بياناتك.")


def find_secrets(text):
    found = []
    for name, pat in SECRET_PATTERNS:
        for m in re.finditer(pat, text):
            if (name == "كلمة سر مكتوبة في الكود" and
                    any(w in m.group(0).lower() for w in PLACEHOLDERS)):
                continue
            found.append((name, m.start(), m.end()))
    return found


def mask_secrets(text):
    for name, a, b in sorted(find_secrets(text), key=lambda x: -x[1]):
        text = text[:a] + "[مخفي]" + text[b:]
    return text


def scan_secrets(text):
    found = find_secrets(text)
    if not found:
        return ("ما لقيت أنماط أسرار معروفة.\n"
                "لكن هذا فحص بسيط، راجع كودك بنفسك قبل الرفع.")
    seen = set()
    lines = []
    for name, a, b in found:
        line = text.count("\n", 0, a) + 1
        if (name, line) not in seen:
            seen.add((name, line))
            lines.append("• السطر %d: %s" % (line, name))
    return ("⚠️ لقيت %d سر محتمل:\n\n" % len(lines) + "\n".join(lines) +
            "\n\nوش تسوي:\n"
            "1) لا ترفع هذا الكود كما هو\n"
            "2) انقل الأسرار لملف إعدادات وضعه في .gitignore\n"
            "3) لو كان سر حقيقي وأرسلته أو رفعته، ألغِه وسوّ بديل")


def translate_error(text):
    low = text.lower()
    hits = [(k, v) for k, v in ERROR_HINTS.items() if k in low]
    words = []
    for w, ar, _ in EN_WORDS:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            words.append("• %s = %s" % (w, ar))
    out = []
    if hits:
        out.append("🔤 شرح الخطأ:\n\n" +
                   "\n\n".join("• %s\n  %s" % (k, v) for k, v in hits))
    if words:
        out.append("📝 كلمات في الرسالة:\n" + "\n".join(words[:10]))
    if not out:
        return ("ما عرفت هذا الخطأ من قاموسي المحلي.\n"
                "اضغط الزر تحت وخلّ Gemini يشرحه لك خطوة بخطوة.")
    return "\n\n".join(out)


# ==================== المعالجات ====================
def show_main(chat):
    u = get_user(chat)
    send(chat, "هلا! أنا بوت حارس 🛡️\nالمستوى %d  %s\n🔥 %d يوم متتالي\n\n"
         "اختر من القائمة:" % (level_of(u["xp"]), bar_of(u["xp"]), u["streak"]),
         MAIN_MENU)


def show_ai_menu(chat, prefix=""):
    u = get_user(chat)
    rows = [
        [btn("🤖 اسأل Gemini", "ask"), btn("🧪 راجع كودي", "review")],
        [btn("🔤 اشرح خطأ", "err"),
         btn("🎚️ الشرح: " + DETAIL_LABELS[u["detail"]], "detail")],
        [HOME],
    ]
    send(chat, prefix + "🤖 Gemini مدرّبك الذكي\nاختر:", rows)


def send_lesson(chat, i):
    nav = []
    if i + 1 < len(LESSONS):
        nav.append(btn("الدرس التالي ➡️", "lesson_" + str(i + 1)))
    nav.append(btn("📘 الدروس", "lessons"))
    u = get_user(chat)
    extra = ""
    if i not in u["lessons"]:
        u["lessons"].append(i)
        extra = "\n\n" + award(chat, LESSON_XP)
    send(chat, "📘 " + LESSONS[i][0] + "\n\n" + LESSONS[i][1] + extra, [nav])


def handle(chat, data):
    if data not in MODES:
        modes[chat] = None

    if data == "menu":
        show_main(chat)

    elif data in SUBMENUS:
        title, rows = SUBMENUS[data]
        send(chat, title + "\nاختر:", rows + [[HOME]])

    elif data == "m_ai":
        show_ai_menu(chat)

    elif data == "detail":
        u = get_user(chat)
        nxt = DETAIL_LEVELS[(DETAIL_LEVELS.index(u["detail"]) + 1)
                            % len(DETAIL_LEVELS)]
        u["detail"] = nxt
        save_data()
        show_ai_menu(chat, "تم: مستوى الشرح = %s\n\n" % DETAIL_LABELS[nxt])

    elif data == "help":
        send(chat, "أوامر سريعة:\n/start القائمة\n/daily تحدي اليوم\n"
             "/profile ملفي\n/ask اسأل Gemini\n/quiz اختبار\n/word كلمة إنجليزية\n"
             "/github GitHub\n/secrets فاحص الأسرار\n\n"
             "المطور: @%s" % DEV_USERNAME, BACK)

    elif data == "dev":
        send(chat, "👨‍💻 المطور: @%s\n\nللملاحظات أو الأخطاء أو الاقتراحات، "
             "راسله مباشرة." % DEV_USERNAME,
             [[{"text": "💬 راسل المطور",
                "url": "https://t.me/" + DEV_USERNAME}], [HOME]])

    elif data == "lessons":
        btns = []
        for i, item in enumerate(LESSONS):
            btns.append([btn(item[0], "lesson_" + str(i))])
        btns.append([HOME])
        send(chat, "📘 اختر الدرس:", btns)

    elif data.startswith("lesson_"):
        send_lesson(chat, int(data.split("_")[1]))

    elif data == "glossary":
        btns = []
        for i, item in enumerate(GLOSSARY):
            btns.append([btn(item[0], "gl_" + str(i))])
        btns.append([HOME])
        send(chat, "📖 اختر المصطلح:", btns)

    elif data.startswith("gl_"):
        item = GLOSSARY[int(data.split("_")[1])]
        send(chat, "📖 " + item[0] + "\n\n" + item[1],
             [[btn("📖 المصطلحات", "glossary"), HOME]])

    elif data == "tip":
        send(chat, "🛡️ " + random.choice(TIPS),
             [[btn("نصيحة ثانية", "tip"), HOME]])

    elif data == "quiz":
        q = random.randrange(len(QUIZ))
        btns = []
        for i, o in enumerate(QUIZ[q][1]):
            btns.append([btn(o, "ans_%d_%d" % (q, i))])
        send(chat, "🧠 " + QUIZ[q][0], btns)

    elif data.startswith("ans_"):
        parts = data.split("_")
        q = int(parts[1])
        i = int(parts[2])
        opts = QUIZ[q][1]
        right = QUIZ[q][2]
        u = get_user(chat)
        u["total"] += 1
        if i == right:
            u["correct"] += 1
            g = quiz_gain(u)
            msg = "✅ صح! أحسنت\n\n" + award(chat, g)
            if g == 0:
                msg += "\n(وصلت سقف نقاط الأسئلة اليوم، ارجع بكرة)"
        else:
            msg = "❌ غلط، الصح: " + opts[right]
            save_data()
        send(chat, msg, [[btn("سؤال ثاني ➡️", "quiz"), HOME]])

    elif data == "daily":
        u = get_user(chat)
        if u["daily"] == today_str():
            send(chat, "🎯 خلصت تحدي اليوم. ارجع بكرة لتحدي جديد.", BACK)
        else:
            q = int(today_str().replace("-", "")) % len(QUIZ)
            btns = []
            for i, o in enumerate(QUIZ[q][1]):
                btns.append([btn(o, "dq_%d_%d" % (q, i))])
            send(chat, "🎯 تحدي اليوم (+%d XP)\n\n%s"
                 % (DAILY_XP, QUIZ[q][0]), btns)

    elif data.startswith("dq_"):
        parts = data.split("_")
        q = int(parts[1])
        i = int(parts[2])
        u = get_user(chat)
        if u["daily"] == today_str():
            send(chat, "🎯 جاوبت تحدي اليوم من قبل. ارجع بكرة.", BACK)
        else:
            u["daily"] = today_str()
            u["total"] += 1
            if i == QUIZ[q][2]:
                u["correct"] += 1
                msg = "✅ صح! أنجزت تحدي اليوم\n\n" + award(chat, DAILY_XP)
            else:
                msg = ("❌ ما صارت، الصح: " + QUIZ[q][1][QUIZ[q][2]] +
                       "\n\n" + award(chat, 3))
            send(chat, msg, BACK)

    elif data in ("word", "word_r"):
        if data == "word":
            w = EN_WORDS[int(today_str().replace("-", "")) % len(EN_WORDS)]
        else:
            w = random.choice(EN_WORDS)
        send(chat, "📝 كلمة اليوم\n\n%s  =  %s\n\nمثال: %s" % (w[0], w[1], w[2]),
             [[btn("🔁 كلمة أخرى", "word_r"), btn("🧩 اختبرني", "wquiz")],
              [HOME]])

    elif data == "wquiz":
        w = random.randrange(len(EN_WORDS))
        others = random.sample([i for i in range(len(EN_WORDS)) if i != w], 2)
        opts = [w] + others
        random.shuffle(opts)
        btns = [[btn(EN_WORDS[o][1], "wq_%d_%d" % (w, o))] for o in opts]
        send(chat, "🧩 وش معنى الكلمة:\n\n%s" % EN_WORDS[w][0], btns)

    elif data.startswith("wq_"):
        parts = data.split("_")
        w = int(parts[1])
        o = int(parts[2])
        u = get_user(chat)
        if w == o:
            u["wcorrect"] += 1
            g = quiz_gain(u)
            msg = "✅ صح! %s = %s\n\n%s" % (EN_WORDS[w][0], EN_WORDS[w][1],
                                           award(chat, g))
        else:
            msg = "❌ غلط، %s = %s" % (EN_WORDS[w][0], EN_WORDS[w][1])
            save_data()
        send(chat, msg, [[btn("كلمة ثانية ➡️", "wquiz"), HOME]])

    elif data == "gen":
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        pw = "".join(secrets.choice(chars) for _ in range(16))
        send(chat, "🔑 كلمة سر قوية:\n\n" + pw + "\n\nاحفظها في مكان آمن.",
             [[btn("ولّد غيرها", "gen"), HOME]])

    elif data == "roadmap":
        send(chat, ROADMAP, BACK)

    elif data == "profile":
        send(chat, profile_text(chat), BACK)

    elif data == "rewards":
        btns = [[{"text": t, "url": u}] for t, u in REWARD_LINKS]
        btns.append([HOME])
        send(chat, REWARDS_TEXT, btns)

    elif data == "res":
        btns = [[btn(v[0], k)] for k, v in RESOURCES.items()]
        btns.append([HOME])
        send(chat, "🎥 الشروحات والقنوات\nاختر القسم:", btns)

    elif data in RESOURCES:
        title, items = RESOURCES[data]
        send(chat, title + "\n\n" + "\n".join(items) + RESOURCES_NOTE,
             [[btn("🎥 الأقسام", "res"), HOME]])

    elif data == "github":
        send(chat, GITHUB_INTRO,
             [[btn("ما هو GitHub", "lesson_9")],
              [btn("أوامر Git الأساسية", "lesson_10")],
              [btn("🔎 فاحص الأسرار", "secrets")],
              [HOME]])

    elif data == "secrets":
        modes[chat] = "secrets"
        send(chat, "🔎 الصق الكود اللي تبي ترفعه وأفحصه عن توكنات ومفاتيح.\n"
             "الفحص يتم داخل البوت ولا يُرسل لأي خدمة خارجية، "
             "وبحذف رسالتك من المحادثة بعد الفحص.", BACK)

    elif data == "ask":
        modes[chat] = "ask"
        history[chat] = []
        send(chat, "🤖 اسألني أي سؤال عن بايثون أو الأمن السيبراني، "
             "واكتب سؤالك الحين:", BACK)

    elif data == "review":
        modes[chat] = "review"
        history[chat] = []
        send(chat, "🧪 أرسل لي كودك (أو الخطأ اللي طلع لك) "
             "وأشرحه معك خطوة بخطوة.", BACK)

    elif data == "link":
        modes[chat] = "link"
        send(chat, "🔗 أرسل الرابط اللي تبي تفحصه "
             "(لا تضغط عليه قبل الفحص).", BACK)

    elif data == "pw":
        modes[chat] = "pw"
        send(chat, "🔐 أرسل كلمة سر تجريبية أفحص قوتها.\n"
             "⚠️ لا تكتب كلمة سرك الحقيقية.", BACK)

    elif data == "err":
        modes[chat] = "err"
        send(chat, "🔤 الصق رسالة الخطأ (بالإنجليزية) وأشرح لك معناها.\n"
             "⚠️ اخفِ التوكن منها قبل اللصق.", BACK)

    elif data == "errai":
        text = last_err.get(chat)
        if not text:
            send(chat, "ما عندي خطأ سابق، الصق الخطأ أول.", BACK)
        else:
            call_typing(chat)
            send(chat, ask_ai(chat, "اشرح لي هذا الخطأ بالعربي خطوة بخطوة "
                              "وقل لي كيف أصلحه:\n" + text, REVIEW_SYSTEM),
                 BACK)

    else:
        show_main(chat)


def call_typing(chat):
    try:
        call("sendChatAction", {"chat_id": chat, "action": "typing"})
    except Exception:
        pass


def on_text(chat, text, mid=None):
    if text.startswith("/"):
        cmd = text.split()[0].split("@")[0].lower()
        handle(chat, CMDS.get(cmd, "menu"))
        return
    mode = modes.get(chat)
    if mode in ("ask", "review"):
        call_typing(chat)
        system = ASK_SYSTEM if mode == "ask" else REVIEW_SYSTEM
        send(chat, ask_ai(chat, mask_secrets(text), system), BACK)
    elif mode == "err":
        last_err[chat] = mask_secrets(text)[:2000]
        send(chat, translate_error(text),
             [[btn("🤖 اشرحه بالتفصيل (Gemini)", "errai")], [HOME]])
    elif mode == "secrets":
        report = scan_secrets(text)
        if mid is not None and delete_message(chat, mid):
            report += "\n\n🧹 حذفت رسالتك من المحادثة."
        if not get_user(chat)["secrets"]:
            get_user(chat)["secrets"] = True
            report += "\n\n" + award(chat, 5)
        send(chat, report, BACK)
    elif mode == "link":
        send(chat, check_link(text), BACK)
    elif mode == "pw":
        send(chat, check_password(text), BACK)
    else:
        show_main(chat)


# ==================== التشغيل ====================
def chat_of(update):
    if "callback_query" in update:
        return update["callback_query"]["message"]["chat"]["id"]
    if "message" in update:
        return update["message"]["chat"]["id"]
    return None


def process(u):
    if "callback_query" in u:
        cq = u["callback_query"]
        try:
            call("answerCallbackQuery", {"callback_query_id": cq["id"]})
        except Exception:
            pass
        handle(cq["message"]["chat"]["id"], cq["data"])
    elif "message" in u and "text" in u["message"]:
        msg = u["message"]
        on_text(msg["chat"]["id"], msg["text"].strip(), msg.get("message_id"))


def main():
    try:
        me = call("getMe")["result"]
        print("✅ متصل باسم @%s" % me.get("username", "?"))
    except urllib.error.HTTPError as e:
        print("❌ التوكن غير صحيح (رمز %d). راجع المتغير TOKEN." % e.code)
        return
    except Exception as e:
        print("❌ تعذّر الاتصال بتيليجرام:", e)
        return
    try:
        call("setMyCommands", {"commands": [
            {"command": c, "description": d} for c, d in BOT_COMMANDS]})
    except Exception:
        pass
    if not GEMINI_KEY:
        print("ℹ️ Gemini غير مفعّل (GEMINI_KEY فاضي)، باقي الميزات تعمل.")
    print("البوت شغّال... (للإيقاف: CTRL + C)")

    offset = 0
    while True:
        try:
            res = call("getUpdates", {
                "offset": offset, "timeout": 30,
                "allowed_updates": ["message", "callback_query"]})
        except urllib.error.HTTPError as e:
            if e.code == 409:
                print("⚠️ في نسخة ثانية من البوت شغّالة بنفس التوكن، أوقفها.")
            else:
                print("خطأ اتصال:", e.code)
            time.sleep(5)
            continue
        except Exception as e:
            print("خطأ اتصال:", e)
            time.sleep(3)
            continue
        for u in res.get("result", []):
            offset = u["update_id"] + 1
            try:
                process(u)
            except Exception:
                traceback.print_exc()
                chat = chat_of(u)
                if chat:
                    try:
                        send(chat, "حصل خطأ بسيط 😅 جرّب مرة ثانية أو اكتب /start",
                             BACK)
                    except Exception:
                        pass


if __name__ == "__main__":
    main()
# النهاية
