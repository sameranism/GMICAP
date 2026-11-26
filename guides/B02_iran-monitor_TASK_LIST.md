# B02 — ایران‌بان (Iran Monitor)

شناسه ثابت بسته: `B02` | مسیر مفهومی: `iran-monitor`
سند مرجع: `source/specs/B02_DOMESTIC_INGEST_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **7**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 2 | `S02-001` | `backend/modules/domestic/feed_client.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-001__feed_client_py.md` |
| 2 | `S02-002` | `backend/modules/domestic/collector.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-002__collector_py.md` |
| 2 | `S02-003` | `backend/modules/domestic/scheduler.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-003__scheduler_py.md` |
| 2 | `S02-004` | `backend/modules/domestic/repository.py` | C | `prompts/02_INGEST_AND_DESIGN/B02/S02-004__repository_py.md` |
| 2 | `S02-005` | `backend/modules/domestic/api.py` | G | `prompts/02_INGEST_AND_DESIGN/B02/S02-005__api_py.md` |
| 2 | `S02-006` | `backend/migrations/domestic/001_ingest.py` | C | `prompts/02_INGEST_AND_DESIGN/B02/S02-006__001_ingest_py.md` |
| 2 | `S02-007` | `backend/tests/test_domestic.py` | C | `prompts/02_INGEST_AND_DESIGN/B02/S02-007__test_domestic_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
