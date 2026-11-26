# B03 — جهان‌بان (Global Monitor)

شناسه ثابت بسته: `B03` | مسیر مفهومی: `global-monitor`
سند مرجع: `source/specs/B03_FOREIGN_INGEST_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **8**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 2 | `S02-008` | `backend/modules/foreign/country_discovery.py` | G | `prompts/02_INGEST_AND_DESIGN/B03/S02-008__country_discovery_py.md` |
| 2 | `S02-009` | `backend/modules/foreign/feed_client.py` | G | `prompts/02_INGEST_AND_DESIGN/B03/S02-009__feed_client_py.md` |
| 2 | `S02-010` | `backend/modules/foreign/collector.py` | G | `prompts/02_INGEST_AND_DESIGN/B03/S02-010__collector_py.md` |
| 2 | `S02-011` | `backend/modules/foreign/bridge.py` | C | `prompts/02_INGEST_AND_DESIGN/B03/S02-011__bridge_py.md` |
| 2 | `S02-012` | `backend/modules/foreign/repository.py` | C | `prompts/02_INGEST_AND_DESIGN/B03/S02-012__repository_py.md` |
| 2 | `S02-013` | `backend/modules/foreign/api.py` | G | `prompts/02_INGEST_AND_DESIGN/B03/S02-013__api_py.md` |
| 2 | `S02-014` | `backend/migrations/foreign/001_ingest.py` | C | `prompts/02_INGEST_AND_DESIGN/B03/S02-014__001_ingest_py.md` |
| 2 | `S02-015` | `backend/tests/test_foreign.py` | C | `prompts/02_INGEST_AND_DESIGN/B03/S02-015__test_foreign_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
