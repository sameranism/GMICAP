# B04 — خبرپرداز (News Processor)

شناسه ثابت بسته: `B04` | مسیر مفهومی: `news-processor`
سند مرجع: `source/specs/B04_PREPROCESSING_TECHNICAL_SPEC.md`

تعداد تسک‌های برنامه: **8**

| مرحله | تسک | فایل خروجی | مدل | پرامپت |
|---:|---|---|---|---|
| 3 | `S03-001` | `backend/modules/processing/extractor.py` | G | `prompts/03_PROCESSING/B04/S03-001__extractor_py.md` |
| 3 | `S03-002` | `backend/modules/processing/normalizer.py` | G | `prompts/03_PROCESSING/B04/S03-002__normalizer_py.md` |
| 3 | `S03-003` | `backend/modules/processing/deduplicator.py` | G | `prompts/03_PROCESSING/B04/S03-003__deduplicator_py.md` |
| 3 | `S03-004` | `backend/modules/processing/classifier.py` | G | `prompts/03_PROCESSING/B04/S03-004__classifier_py.md` |
| 3 | `S03-005` | `backend/modules/processing/router.py` | C | `prompts/03_PROCESSING/B04/S03-005__router_py.md` |
| 3 | `S03-006` | `backend/modules/processing/repository.py` | C | `prompts/03_PROCESSING/B04/S03-006__repository_py.md` |
| 3 | `S03-007` | `backend/migrations/central/002_processing.py` | C | `prompts/03_PROCESSING/B04/S03-007__002_processing_py.md` |
| 3 | `S03-008` | `backend/tests/test_processing.py` | C | `prompts/03_PROCESSING/B04/S03-008__test_processing_py.md` |

**قاعده:** پیش از ویرایش، ورودی‌های هر تسک در فایل `__ATTACHMENTS.txt` کنار پرامپت مشخص است.
**مرز:** خروجی‌ها فقط با API/Event نسخه‌دار و مجوز به بسته دیگر منتقل شوند.
