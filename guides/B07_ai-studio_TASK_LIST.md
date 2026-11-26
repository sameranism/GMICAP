# B07 — آوانما (AI News Studio)

شناسه ثابت بسته: `B07` | مسیر مفهومی: `ai-studio`
سند مرجع: `source/specs/B07_STUDIO_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **6**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 7 | `S07-001` | `backend/modules/studio/tts.py` | G | `prompts/07_STUDIO/B07/S07-001__tts_py.md` |
| 7 | `S07-002` | `backend/modules/studio/subtitles.py` | G | `prompts/07_STUDIO/B07/S07-002__subtitles_py.md` |
| 7 | `S07-003` | `backend/modules/studio/renderer.py` | G | `prompts/07_STUDIO/B07/S07-003__renderer_py.md` |
| 7 | `S07-004` | `backend/modules/studio/repository.py` | C | `prompts/07_STUDIO/B07/S07-004__repository_py.md` |
| 7 | `S07-005` | `backend/migrations/central/006_studio.py` | C | `prompts/07_STUDIO/B07/S07-005__006_studio_py.md` |
| 7 | `S07-006` | `backend/tests/test_studio.py` | C | `prompts/07_STUDIO/B07/S07-006__test_studio_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
