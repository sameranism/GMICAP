# B06 — ژرفان (Intelligence & Reports)

شناسه ثابت بسته: `B06` | مسیر مفهومی: `intelligence`
سند مرجع: `source/specs/B06_INTELLIGENCE_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **10**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 5 | `S05-001` | `backend/modules/intelligence/analysis.py` | G | `prompts/05_INTELLIGENCE/B06/S05-001__analysis_py.md` |
| 5 | `S05-002` | `backend/modules/intelligence/evidence.py` | C | `prompts/05_INTELLIGENCE/B06/S05-002__evidence_py.md` |
| 5 | `S05-003` | `backend/modules/intelligence/retrieval.py` | C | `prompts/05_INTELLIGENCE/B06/S05-003__retrieval_py.md` |
| 5 | `S05-004` | `backend/modules/intelligence/chat.py` | G | `prompts/05_INTELLIGENCE/B06/S05-004__chat_py.md` |
| 5 | `S05-005` | `backend/modules/intelligence/metrics.py` | G | `prompts/05_INTELLIGENCE/B06/S05-005__metrics_py.md` |
| 5 | `S05-006` | `backend/modules/intelligence/public_reports.py` | G | `prompts/05_INTELLIGENCE/B06/S05-006__public_reports_py.md` |
| 5 | `S05-007` | `backend/modules/intelligence/private_reports.py` | C | `prompts/05_INTELLIGENCE/B06/S05-007__private_reports_py.md` |
| 5 | `S05-008` | `backend/modules/intelligence/repository.py` | C | `prompts/05_INTELLIGENCE/B06/S05-008__repository_py.md` |
| 5 | `S05-009` | `backend/migrations/central/004_intelligence.py` | C | `prompts/05_INTELLIGENCE/B06/S05-009__004_intelligence_py.md` |
| 5 | `S05-010` | `backend/tests/test_intelligence.py` | C | `prompts/05_INTELLIGENCE/B06/S05-010__test_intelligence_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
