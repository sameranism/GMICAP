# B08 — رسان (Publishing Engine)

شناسه ثابت بسته: `B08` | مسیر مفهومی: `publishing`
سند مرجع: `source/specs/B08_PUBLISHING_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **15**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 6 | `S06-001` | `backend/modules/publishing/scheduler.py` | C | `prompts/06_PUBLISHING/B08/S06-001__scheduler_py.md` |
| 6 | `S06-002` | `backend/modules/publishing/destinations.py` | C | `prompts/06_PUBLISHING/B08/S06-002__destinations_py.md` |
| 6 | `S06-003` | `backend/modules/publishing/formatter.py` | G | `prompts/06_PUBLISHING/B08/S06-003__formatter_py.md` |
| 6 | `S06-004` | `backend/modules/publishing/dispatcher.py` | C | `prompts/06_PUBLISHING/B08/S06-004__dispatcher_py.md` |
| 6 | `S06-005` | `backend/adapters/base.py` | C | `prompts/06_PUBLISHING/B08/S06-005__base_py.md` |
| 6 | `S06-006` | `backend/adapters/telegram.py` | G | `prompts/06_PUBLISHING/B08/S06-006__telegram_py.md` |
| 6 | `S06-007` | `backend/adapters/bale.py` | G | `prompts/06_PUBLISHING/B08/S06-007__bale_py.md` |
| 6 | `S06-008` | `backend/adapters/eitaa.py` | G | `prompts/06_PUBLISHING/B08/S06-008__eitaa_py.md` |
| 6 | `S06-009` | `backend/adapters/rubika.py` | G | `prompts/06_PUBLISHING/B08/S06-009__rubika_py.md` |
| 6 | `S06-010` | `backend/adapters/whatsapp.py` | G | `prompts/06_PUBLISHING/B08/S06-010__whatsapp_py.md` |
| 6 | `S06-011` | `backend/adapters/cms.py` | C | `prompts/06_PUBLISHING/B08/S06-011__cms_py.md` |
| 6 | `S06-012` | `backend/adapters/registry.py` | C | `prompts/06_PUBLISHING/B08/S06-012__registry_py.md` |
| 6 | `S06-013` | `backend/modules/publishing/repository.py` | C | `prompts/06_PUBLISHING/B08/S06-013__repository_py.md` |
| 6 | `S06-014` | `backend/migrations/central/005_publishing.py` | C | `prompts/06_PUBLISHING/B08/S06-014__005_publishing_py.md` |
| 6 | `S06-015` | `backend/tests/test_publishing.py` | C | `prompts/06_PUBLISHING/B08/S06-015__test_publishing_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
