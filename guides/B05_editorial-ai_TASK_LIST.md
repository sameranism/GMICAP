# B05 — نگار (Editorial AI)

شناسه ثابت بسته: `B05` | مسیر مفهومی: `editorial-ai`
سند مرجع: `source/specs/B05_CONTENT_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **9**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 4 | `S04-001` | `backend/modules/editorial/glossary.py` | C | `prompts/04_EDITORIAL/B05/S04-001__glossary_py.md` |
| 4 | `S04-002` | `backend/modules/editorial/policy.py` | C | `prompts/04_EDITORIAL/B05/S04-002__policy_py.md` |
| 4 | `S04-003` | `backend/modules/editorial/quality.py` | C | `prompts/04_EDITORIAL/B05/S04-003__quality_py.md` |
| 4 | `S04-004` | `backend/modules/editorial/translator.py` | G | `prompts/04_EDITORIAL/B05/S04-004__translator_py.md` |
| 4 | `S04-005` | `backend/modules/editorial/editor.py` | G | `prompts/04_EDITORIAL/B05/S04-005__editor_py.md` |
| 4 | `S04-006` | `backend/modules/editorial/image_processor.py` | G | `prompts/04_EDITORIAL/B05/S04-006__image_processor_py.md` |
| 4 | `S04-007` | `backend/modules/editorial/repository.py` | C | `prompts/04_EDITORIAL/B05/S04-007__repository_py.md` |
| 4 | `S04-008` | `backend/migrations/central/003_editorial.py` | C | `prompts/04_EDITORIAL/B05/S04-008__003_editorial_py.md` |
| 4 | `S04-009` | `backend/tests/test_editorial.py` | C | `prompts/04_EDITORIAL/B05/S04-009__test_editorial_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
