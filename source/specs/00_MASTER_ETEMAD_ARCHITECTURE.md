# 00_MASTER_ETEMAD_ARCHITECTURE


> Extracted without semantic modification from `00_MASTER_ETEMAD_ARCHITECTURE.docx`. If ambiguous, consult the original DOCX.


سند مادر معماری و قراردادهای اجرایی

## مبنای مشترک برای ۹ تیم و ۲۹ پروژه | MASTER SPECIFICATION

نسخه 1.1  |  ۳۰ آبان ۱۴۰۵ / ۲۱ نوامبر ۲۰۲۶  |  وضعیت: مشخصات طراحی، نه سامانه عملیاتی

## ۱. خلاصه تصمیم‌های کارفرما

| موضوع | تصمیم مصوب / قید |

| --- | --- |

| فناوری | Python/FastAPI، PostgreSQL، Redis، React/TypeScript؛ مدل‌های AI از طریق Gateway قابل تعویض |

| استقرار | یک محیط مستقل داخلی، یک محیط مستقل خارجی، یک هسته مرکزی مشترک با انتقال امن |

| ظرفیت | ۵۰۰ تا ۵۰۰۰ خبر ورودی در روز؛ جداسازی بار AI از رصد و انتشار |

| CMS | نامشخص؛ P23/P25 باید Adapter قابل تعویض داشته باشند |

| مقاصد مرحله اول | Telegram، Bale، Eitaa، Rubika، WhatsApp Business و سایر مقصدهای قابل توسعه؛ تنها در صورت API و مجوز معتبر |

| کاربران | سقف ۱۰ حساب انسانی فعال؛ دو داشبورد ممتاز owner و editor_in_chief و نماهای کارکنان |

| برند | استایل وزین فارسی RTL و تطبیق با لوگو/رنگ رسمی روزنامه اعتماد؛ اصل دارایی برند هنوز ارائه نشده |

| امنیت و قانون | قواعد نشر داخلی ایران + تأیید حقوقی قبل از بهره‌برداری؛ حفظ منبع و حق بازنشر |

| گزارش‌ها | ۴ عمومی قابل انتشار پس از P11 + ۳ خصوصی صرفاً مدیرمسئول |

| خاموشی مستقل | public_analysis، studio(audio/video)، publishing(domestic/foreign/reports) |

## ۲. مرز سیستم، ۶ لایه و ۹ بسته

| شناسه بسته | نام | مسئولیت | محیط |

| --- | --- | --- | --- |

| B01 | بنیان | قرارداد داده، منبع، تنظیمات، هویت، آرشیو و هماهنگی را به‌صورت سرویس‌های مستقل و قابل آزمون فراهم می‌کند. | مشترک / هسته مرکزی |

| B02 | ایران‌بان | دریافت و پایش منابع داخلی با صف، زمان‌بندی و پایگاه داده جدا از رصد خارجی. | محیط داخلی مستقل |

| B03 | جهان‌بان | کشف فید رسانه‌های کشورها و جمع‌آوری خبر خارجی با درگاه انتقال امن. | محیط خارجی مستقل |

| B04 | خبرپرداز | پاک‌سازی، یکتاسازی و مسیر‌دهی اخبار به سرویس‌های تخصصی. | پردازش مشترک هسته |

| B05 | نگار | اجرای قواعد واژگان و قوانین محتوا، ترجمه، بازنویسی و تصویرسازی مناسب خبر. | پردازش مشترک هسته |

| B06 | ژرفان | تحلیل مستند و بی‌طرفانه، چت‌بات فقط در بخش تحلیل، شاخص‌ها و هفت گزارش روزانه. | تحلیل مشترک؛ حریم خصوصی جدا |

| B07 | آوانما | گوینده صوتی و مجری مجازی خبر، قابل خاموش‌کردن مستقل از پردازش متن. | سرویس خروجی مستقل |

| B08 | رسان | ثبت مقصدها، صف و زمان‌بندی، قالب‌بندی اختصاصی و ارسال هم‌زمان. | سرویس خروجی مستقل |

| B09 | دیدبان | رابط فارسی RTL با دو داشبورد ویژه و نماهای تخصصی با مجوز سمت سرور. | رابط واحد وب |

مرزبندی ۶ لایه مصوب: رصد داخلی؛ رصد خارجی؛ پردازش محتوا؛ تحلیل و گزارش؛ استودیو و انتشار؛ بستر مرکزی. بسته‌های B01 تا B09 واحدهای تحویل هستند و لزوماً ۹ سرور مستقل نیستند.

## ۳. مدل استقرار و مسیر داده

•  سرور داخلی: پایگاه و صف ingest داخلی با منابع ایرانی؛ snapshot پیکربندی از P03؛ هر raw item با id و fingerprint.

•  سرور خارجی: پایگاه و صف ingest خارجی؛ کشف کشورها P04؛ خروجی raw_news از Bridge امضاشده/احراز هویت‌شده.

•  هسته مرکزی: ۱ PostgreSQL با schemaهای مالکیت‌دار؛ Redis Streams یا صف worker؛ مخزن فایل سازگار S3؛ API Gateway و P28.

•  جهت جریان: P05/P06 → P07 → P08 → P09 → P12/P13/P14 → P11 → P22/P24/P25 → P26/P17.

•  جهت گزارش: P26 + P15/P17 → P18 → P11 → P22 یا P19 → مخزن executive_private (بدون publication).

•  مسیر استودیو: متن عمومی تأییدشده → P20 → P21 اختیاری → P24/P25، با کنترل خروجی در هر لحظه.

•  تمام رویدادها با event_id/correlation_id/idempotency_key؛ payload کامل فقط در Artifact Store؛ رویداد حامل reference.

## ۴. پایگاه داده و مالکیت اطلاعات

پایگاه داده پیشنهادی شامل سه استقرار PostgreSQL است: etemad_domestic در سرور داخلی، etemad_foreign در سرور خارجی و etemad_core در مرکز. جدول‌های مرکزی در schemaهای مالکیت‌دار ساخته می‌شوند. هر بسته فقط حق نوشتن در schema خود را دارد. خواندن اطلاعات سایر بسته‌ها از API یا رویداد با احراز هویت انجام می‌شود.

| محیط | schema / مثال | مالک |

| --- | --- | --- |

| هسته | identity, control, sources, archive, orchestration, security | B01 |

| داخلی | domestic.* | B02 |

| خارجی | foreign.* | B03 |

| هسته | processing.* | B04 |

| هسته | editorial.* | B05 |

| هسته و محدوده خصوصی | insights.* و executive.private_reports | B06 |

| هسته | studio.* | B07 |

| هسته | publish.* | B08 |

| هسته | ui.saved_views / preferences | B09 |

برای گزارش‌های خصوصی، schema اجرایی در database مجزا یا role و bucket ایزوله با RLS/GRANT سخت‌گیرانه مستقر شود. هیچ join عمومی یا replica عمومی از این داده مجاز نیست. امکان‌سنجی پایگاه مجزای خصوصی پیش از تولید الزامی است.

## ۵. جدول‌های پیشنهادی و کلیدهای اصلی

## B01 — بنیان

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| control.config_revisions | P02 | config_id, version_no, scope, value_json, changed_by, effective_at \| UNIQUE(config_id,version_no)؛ تغییرات immutable |

| control.output_switches | P02 | switch_key, scope, enabled, revision, updated_by, updated_at \| UNIQUE(switch_key,scope)؛ پیش از side effect خوانده شود |

| control.editorial_rules | P02/P10 | rule_id, revision, desk, kind, rule_json, approved_by \| نسخه‌بندی و ارجاع به قواعد، بدون تغییر متن منبع |

| sources.source_registry | P03 | source_id, country, stream, url, mode, language, rights_scope, state \| UNIQUE(stream,url_normalized)؛ API keys فقط credential_ref |

| identity.users | P28 | user_id, username, role_id, password_hash, must_reset, is_active, created_at \| سقف ۱۰ حساب انسانی فعال؛ گذرواژه هش‌شده؛ مجوز مدیریت کاربران |

| identity.roles_permissions | P28 | role_id, permission_key, resource_scope, condition_json \| کلید(role_id,permission_key,resource_scope) |

| identity.auth_sessions | P28 | session_id, user_id, expires_at, revoked_at, client_fingerprint \| جلسه کوتاه‌عمر + MFA نقش ممتاز؛ audit |

| archive.news_records | P26 | news_id, stream, source_id, title, source_ref, published_at, received_at, classification \| UNIQUE(news_id)؛ شاخص(stream,published_at)؛ متن منبع immutable |

| archive.artifact_index | P26 | artifact_id, object_type, owner_project, object_uri, sha256, visibility, created_at \| صرفاً URI امن؛ فایل بزرگ در Object Store |

| orchestration.jobs | P29 | job_id, type, project_id, state, idempotency_key, attempts, deadline_at \| UNIQUE(project_id,idempotency_key)؛ retry bounded |

| orchestration.outbox | P29 | event_id, topic, aggregate_id, payload_ref, published_at, created_at \| Transactional Outbox و نگهداری محدود |

| security.audit_log | P28 | audit_id, actor_id, action, object_type, object_id, time, reason \| append-only؛ پاک‌کردن توسط نقش عملیاتی ممنوع |

## B02 — ایران‌بان

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| domestic.sources_snapshot | P05 | source_id, version, url, mode, poll_interval_s, enabled \| نسخه local snapshot از P03 |

| domestic.poll_state | P05 | source_id, etag, last_modified, last_success_at, next_poll_at \| UNIQUE(source_id)؛ conditional HTTP GET |

| domestic.raw_items | P05 | raw_id, source_id, source_url, fetched_at, content_ref, source_hash, state \| UNIQUE(source_id,source_hash)؛ متن مجاز در ذخیره‌ساز محلی |

## B03 — جهان‌بان

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| foreign.source_candidates | P04 | candidate_id, country_code, title, site_url, feed_url, verified, evidence_uri \| بازبینی ادمین پیش از افزودن به P03 |

| foreign.poll_state | P06 | source_id, etag, last_modified, last_success_at, next_poll_at \| UNIQUE(source_id)؛ استقلال صف خارجی |

| foreign.raw_items | P06 | raw_id, source_id, country_code, source_url, fetched_at, content_ref, source_hash \| UNIQUE(source_id,source_hash)؛ ارسال فقط از Bridge |

## B04 — خبرپرداز

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| processing.normalized_items | P07 | news_id, raw_ref, title, body_ref, lang, source_country, subject_countries, quality \| source immutable, version of extraction recorded |

| processing.clusters | P08 | cluster_id, canonical_id, similarity_version, updated_at \| نگه‌داشت منابع متعارض به‌صورت مستقل |

| processing.cluster_members | P08 | cluster_id, news_id, score, relation \| UNIQUE(cluster_id,news_id) |

| processing.news_desks | P09 | news_id, desk_id, priority_reason, version, selected \| UNIQUE(news_id,desk_id)؛ سیاست داخلی/خارجی مستقل |

## B05 — نگار

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| editorial.rulesets | P10 | ruleset_id, revision, locale, desk, terms_ref, policy_ref, approved_at \| نقل‌قول‌ها هرگز auto_replace نشوند |

| editorial.policy_decisions | P11 | decision_id, object_id, decision, reasons_json, policy_revision, decided_at \| UNIQUE(object_id,policy_revision,content_hash) |

| editorial.translations | P12 | translation_id, news_id, input_hash, lang_pair, model_ref, text_ref, qa_json \| نگهداری متن اصلی و ارجاع ترجمه |

| editorial.articles | P13 | article_id, news_id, desk_id, version, content_ref, summary_ref, state \| UNIQUE(article_id,version)؛ revisionهای غیرقابل ویرایش |

| editorial.image_assets | P14 | image_id, article_id, media_ref, rights_ref, rendition_json, approval \| حفظ حقوق تصویر و منشأ AI |

## B06 — ژرفان

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| insights.analyses | P15 | analysis_id, topic, period_start, period_end, evidence_ref, confidence_note \| اسناد/نقل‌قول‌ها و فرضیه جدا |

| insights.chat_sessions | P16 | chat_id, user_id, scope, started_at, state \| RLS/RBAC قبل از retrieval |

| insights.chat_messages | P16 | message_id, chat_id, actor, text_ref, evidence_ref, created_at \| داده محرمانه بدون دسترسی در prompt نیست |

| insights.metric_snapshots | P17 | snapshot_id, stream, desk, metric_date, value_json, data_cutoff \| UNIQUE(stream,desk,metric_date,snapshot_type) |

| insights.public_reports | P18 | report_id, report_slot, report_day, revision, content_ref, validation_state \| UNIQUE(report_day,report_slot,revision)؛ slot 1..4 |

| executive.private_reports | P19 | report_id, report_slot, report_day, content_ref, owner_id, restricted_at \| slot 5..7؛ DB role و bucket خصوصی؛ publishable=false |

## B07 — آوانما

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| studio.audio_jobs | P20 | audio_id, article_id, text_hash, voice_ref, artifact_ref, review_state \| اطلاعات صدای مجاز و متن خوانده‌شده |

| studio.video_jobs | P21 | video_id, audio_id, avatar_ref, scene_ref, artifact_ref, synthetic_label \| ثبت هویت مجری مصنوعی و watermark |

## B08 — رسان

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| publish.destinations | P23 | destination_id, provider, channel_ref, stream, desk, credential_ref, verified \| UNIQUE(provider,channel_ref)؛ credential امن و مجوز تست‌شده |

| publish.jobs | P22 | job_id, article_id, report_id, stream, deadline_at, schedule_at, state, policy_decision_id \| UNIQUE(publication_intent_key)؛ تاریخ انقضا |

| publish.payloads | P24 | payload_id, job_id, destination_id, message_ref, image_ref, payload_hash \| UNIQUE(job_id,destination_id)؛ rendition سازگار |

| publish.attempts | P25 | attempt_id, job_id, destination_id, status, provider_msg_id, started_at, ended_at \| UNIQUE(job_id,destination_id,attempt_no)؛ وضعیت unknown مهار شود |

## B09 — دیدبان

| جدول | مالک | فیلدهای پایه / قید |

| --- | --- | --- |

| ui.saved_views | P27 | view_id, user_id, dashboard_type, filters_json, created_at \| dashboard_type owner/editor_in_chief/staff |

| ui.notification_preferences | P27 | user_id, scope, channels_json, enabled \| مالکیت preference نزد UI؛ حق دسترسی نزد P28 |

## ۶. قرارداد استاندارد پیام، فایل و API

•  JSON Schema Draft 2020-12 و نمونه‌های v1.0 ضمیمه، مبنای اعتبارسنجی پیام‌ها هستند؛ نسخه داده در schema_version اجباری است.

•  هر رویداد: event_id، correlation_id، idempotency_key، timestamp UTC، object_id، type، stream، classification، payload_ref.

•  خطاها: HTTP 400 contract_invalid، 401 unauthorized، 403 forbidden، 409 conflict، 422 invalid_state، 429 rate_limited، 503 dependency_unavailable؛ body شامل code/message/correlation_id.

•  برون‌داد هر پروژه دارای producer_project, schema_version, payload checksum, classification و content provenance است.

•  نقش‌های privileged از MFA استفاده کنند؛ دسترسی بین سرویس‌ها به‌صورت identity مجزا؛ رویداد private در queue خصوصی.

•  افزودن فیلد اختیاری سازگار است؛ تغییر نوع/معنا یا حذف فیلد اجباری نیاز به قرارداد major جدید و دوره migration دارد.

## ۷. فهرست ۲۹ پروژه و مسیر ارتباط

| پروژه | نام | مالک بسته | ورودی | خروجی |

| --- | --- | --- | --- | --- |

| P01 | استاندارد داده | B 0 | نیاز سایر بخش‌ها | schemas/*.schema.json |

| P02 | تنظیمات مدیریتی | B 0 | درخواست مدیر/قواعد | output_controls و تنظیمات نسخه‌دار |

| P03 | مدیریت منابع | B 0 | URL/RSS/API/کشور | source_registry |

| P04 | کشف رسانه کشورها | B 0 | نام کشور/قید زبان | country_source_pack |

| P05 | دریافت داخلی | B 0 | فهرست منابع داخلی | raw_news:domestic |

| P06 | دریافت خارجی | B 0 | فهرست منابع خارجی | raw_news:foreign |

| P07 | استانداردسازی | B 0 | raw_news | normalized_news |

| P08 | تشخیص تکرار | B 0 | normalized_news/آرشیو | cluster_result |

| P09 | دسته‌بندی سرویس‌ها | B 0 | خبر و خوشه | classified_news |

| P10 | چارچوب/واژه‌نامه | B 0 | قواعد و سبک | editorial_rules نسخه‌دار |

| P11 | کنترل محتوا و انتشار | B 0 | article/public_report/حقوق | validation_decision |

| P12 | مترجم هوشمند | B 0 | خبر خارجی/واژه‌نامه | translation |

| P13 | ویراستار | B 0 | خبر/ترجمه/چارچوب | article |

| P14 | آماده‌سازی تصویر | B 0 | تصویر/لوگو/قالب | image_manifest |

| P15 | تحلیل سیاسی | B 0 | خبر/آرشیو/بازه | analysis_result |

| P16 | چت‌بات تحلیل | B 0 | سؤال/اسناد مجاز | analysis_chat_response |

| P17 | شاخص‌ها | B 0 | آرشیو/انتشار/بازه | metrics_snapshot |

| P18 | چهار گزارش عمومی | B 0 | آرشیو/شاخص/زمان | public_report |

| P19 | سه گزارش اختصاصی | B 0 | تحلیل/آرشیو/مجوز | private_report |

| P20 | گوینده هوشمند | B 0 | article/public_report | audio_manifest |

| P21 | مجری مجازی استودیو | B 0 | صوت/زیرنویس/قالب | video_manifest |

| P22 | زمان‌بندی | B 0 | validation_decision/زمان | publication_job |

| P23 | مقاصد انتشار | B 0 | پلتفرم/credential_ref | destination_config |

| P24 | قالب‌بندی مقصد | B 0 | خبر/تصویر/مقصد | destination_payloads |

| P25 | ارسال چندکاناله | B 0 | publication_job/payload | publication_result |

| P26 | آرشیو | B 0 | خبر/گزارش/نتیجه | API و شناسه شیء |

| P27 | داشبوردها | B 0 | شاخص/وضعیت/مجوز | رابط واحد |

| P28 | کنترل دسترسی | B 0 | هویت/نقش/منبع | access_decision |

| P29 | هماهنگ‌کننده | B 0 | رویداد/وضعیت | event_envelope/Workflow |

## ۸. مدل هویت و دو داشبورد ممتاز

•  owner: دسترسی به سلامت پلتفرم، تنظیمات فنی، بودجه، کاربران و مقصدها؛ اجازه مشاهده گزارش‌های محرمانه ندارد مگر با grant مستقل ثبت‌شده (پیش‌فرض ممنوع).

•  editor_in_chief: دسترسی تحریریه، ۷ گزارش از جمله سه گزارش private و تأیید موارد استثنایی؛ دسترسی به کلید خام API ندارد.

•  staff: حداکثر ۸ حساب دیگر، هر حساب شخصی با نقش desk/editor/translator/analyst/publisher/technical به تناسب نیاز.

•  ثبت حساب: تولید رمز اولیه تصادفی قوی به‌ازای هر فرد در سرور؛ تحویل یک‌باره در کانال امن، ذخیره Argon2id hash، تغییر اجباری اولین ورود، MFA برای دو نقش ممتاز.

•  هیچ رمز ثابت یا مشترک، رمز واقعی یا کلید API در این بسته اسناد نوشته نشده است؛ احراز هویت سمت سرور و نشست‌های کوتاه‌عمر الزامی است.

•  سقف ۱۰ حساب انسانی فعال با transaction و قفل/constraint سطح سرویس enforce شود؛ حساب سرویس با human seat ترکیب نشود.

## ۹. خروجی‌های اختیاری و رفتار توقف

| کلید | در حالت off | عملیات ادامه‌دار |

| --- | --- | --- |

| public_analysis.enabled | P18 تولید ۴ گزارش جدید را آغاز نمی‌کند | P15/P17/P19 و رصد و آرشیو |

| studio.enabled | P20/P21 job جدید نمی‌پذیرند | انتشار متنی و تحلیل |

| studio.audio_enabled | کار جدید TTS متوقف | ویدئو وابسته به صوت جدید تولید نشود |

| studio.video_enabled | کار جدید ویدئو متوقف | صوت در صورت فعال بودن |

| publishing.enabled | P25 هیچ ارسال خارجی جدید انجام نمی‌دهد | رصد، آرشیو، پردازش، گزارش خصوصی |

| publishing.domestic_enabled | ارسال جریان داخلی متوقف | ارسال جریان خارجی مجاز |

| publishing.foreign_enabled | ارسال جریان خارجی متوقف | ارسال داخلی مجاز |

| publishing.public_reports_enabled | ارسال چهار گزارش عمومی متوقف | انتشار خبر مجاز و گزارش خصوصی |

نکته: خاموشی باید قبل از side effect خارجی دوباره بررسی شود؛ job معلق پس از روشن‌شدن خودکار ارسال نمی‌شود مگر زمان، rights، policy و revision هنوز معتبر باشند. عدم اجرای fallback ناخواسته برای private یک invariant ثابت است.

## ۱۰. سیاست تحریریه و الزامات حقوقی

قواعد مورد درخواست کارفرما به‌عنوان policy-as-data پیاده‌سازی می‌شوند، نه فهرست ثابت کلمات ممنوعه. قوانین و سیاست تحریریه از هم تفکیک شده‌اند و برای هر قاعده، شناسه، نسخه، بازه اعتبار، ارجاع حقوقی، اقدام و نقش تأییدکننده ثبت می‌شود.

•  ارزیابی موضوعات توهین و تبعیض علیه دین، مذهب، قومیت و گروه‌ها، افترا، ادعاهای خلاف واقع، محرمانگی اسناد و مجوز بازنشر باید به زمینه محتوا وابسته باشد.

•  تفاوت گزارش مستند درباره یک سخن توهین‌آمیز با تأیید/تکرار توهین به‌عنوان موضع رسانه حفظ شود.

•  تغییر نام یا لقب سیاسی/مذهبی در متن فقط در صورت همخوانی واقعی و زمانی؛ نقل‌قول مستقیم و اصل منبع تغییر نکنند.

•  اصلاح خودکار پست منتشرشده مطابق تصمیم کارفرما در دامنه این نسخه نیست؛ اما log، نسخه و مسیر پیگیری حقوقی دستی باید محفوظ باشد.

•  پیش از انتشار عملیاتی، متن روزآمد قانون و وضعیت مجوزهای رسانه توسط مشاور حقوقی یا مسئول ذی‌صلاح بازبینی و امضا شود؛ سند جایگزین نظر حقوقی نیست.

| منبع بررسی حقوقی | کاربرد | نشانی |

| --- | --- | --- |

| قانون مطبوعات | چارچوب مواد مرتبط با حقوق اشخاص، افترا، محتوای محدودشده و حق پاسخ؛ بررسی نسخه جاری ضروری است | https://law-ir.ir/law/cat/1925/ |

| قانون جرایم رایانه‌ای | بررسی حدود انتشار مطالب خلاف واقع، دسترسی غیرمجاز و الزامات مرتبط با خدمات آنلاین | https://law-ir.ir/law/cat/1644/ |

| آیین‌نامه‌ها و مجوز رسانه | تعیین وضع مجوز رسانه/سایت و شرایط اختصاصی توسط مسئول حقوقی پیش از بهره‌برداری | نیازمند شناسایی پروانه/مجوز واقعی رسانه |

| حقوق نشر و قرارداد منبع | اجازه دریافت، ترجمه، آرشیو و بازنشر هر منبع باید جداگانه ثبت شود | قرارداد رسانه/منبع؛ هنوز ارائه نشده |

## ۱۱. معماری رابط و نظام هویت بصری

•  React + TypeScript + Mantine با پشتیبانی RTL؛ TanStack Query برای وضعیت server؛ ECharts برای نمودار و React Flow برای شبکه منابع/فرآیند.

•  طرح متمایز، وزین و کم‌ازدحام: زمینه عاجی، متن زغالی، تأکید سرخ تیره و طلایی محدود؛ رنگ‌ها فعلاً نمونه‌اند، نه هویت برند رسمی.

•  لوگوی واقعی و فایل‌های مجاز روزنامه اعتماد باید از کارفرما دریافت شوند؛ تا آن زمان فقط placeholder تایپوگرافیک «اعتماد» استفاده شود.

•  داشبورد owner و editor_in_chief مستقل در routing/navigation و server scope؛ داشبورد کارکنان به تناسب نقش.

•  گروه صفحات: رصد داخلی، خارجی، سرویس‌های تخصصی، نگار، تحلیل سیاسی/چت، استودیو، مقصدها، انتشار، گزارش‌ها و تنظیمات.

•  سنجش Accessibility (keyboard, contrast)، نمایش موبایل، فارسی/انگلیسی مختلط، تاریخ شمسی در UI و UTC در DB.

## ۱۲. آزمون‌های میان‌تیمی و پذیرش

•  تمام ۳۰ مثال schema مبنا معتبر باشند و تمام نمونه‌های ناسازگار مشخصاً رد شوند.

•  Bridge سرور خارجی با credential نامعتبر یا تغییر checksum reject شود؛ DB مرکزی از آن محیط مستقیم در دسترس نباشد.

•  پروژه P19 و report_private حتی با جعل درخواست POST /publishing/jobs وارد صف P25 نشوند.

•  تست خاموشی سه خروجی به‌صورت مستقل در حین وجود job معلق و در هنگام درخواست خارجی.

•  کارمند با URL مستقیم به صفحه محرمانه یا API محدود پاسخ 403 بگیرد؛ حق دسترسی owner به private پیش‌فرض رد شود.

•  مجموع pipeline با ۵۰۰۰ خبر/روز و burst فرضی آزمایش شود؛ هزینه token، تأخیر translation و تعداد queue workers اندازه‌گیری شود.

•  نصب و تست CMS / مقصدهای خارجی صرفاً پس از دریافت اعتبارنامه مجاز و انتخاب CMS انجام گیرد.

## ۱۳. ریسک‌ها و موضوعات باز برای قرارداد اجرای واقعی

| موضوع باز | تصمیم پیش‌فرض تا زمان تعیین |

| --- | --- |

| CMS وب‌سایت | Adapter عمومی + mock؛ هیچ CMS خاصی فرض نشده |

| توکن‌ها و آدرس کانال‌ها | credential_ref placeholder؛ API هر مقصد جداگانه نیازمند تست واقعی |

| لوگوی رسمی و راهنمای برند | پالت موقت؛ هیچ فایل لوگوی رسمی در بسته وجود ندارد |

| سیاست حقوقی نهایی | قواعد نمونه + امضای مسئول حقوقی پیش از production |

| میزبانی/شبکه و محل داده | سه محیط منطقی/فیزیکی مفروض؛ نیازمند مشخصات میزبان، VPN و DNS |

| تعداد دقیق کارکنان و نقش‌ها | ۱۰ حساب کل با ۲ نقش ویژه و ۸ حساب با نقش قابل تعریف |

| هزینه و سقف AI | multi-provider gateway با تنظیم budget و usage log؛ سقف مالی تعیین نشده |

## ۱۴. قاعده تحویل به تیم‌ها

هر تیم علاوه بر سند همین بسته باید به قرارداد JSON Schema، شناسنامه Pهای مالک، نمونه‌های معتبر و تست‌های مرز دسترسی دسترسی داشته باشد. هیچ تیمی مجاز به ایجاد جدول یا خواندن DB تحت مالکیت بسته دیگر نیست مگر از API/event versioned. هر تغییر قراردادی نیازمند ADR، تست سازگاری، release note و بازه migration است.
