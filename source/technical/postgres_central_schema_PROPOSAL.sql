-- ETEMAD architecture v1.1: typed PostgreSQL DDL proposal (development reference)
-- NOT a finalized production migration. Security policies, row access rules, relationships,
-- retention and official editorial policy must be reviewed by DB/security/legal teams.
-- Contract-level IDs are TEXT because v1.0 examples use readable string identifiers.
-- Application secrets and password plaintext must never be written to these tables.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS control;
-- P02 | UNIQUE(config_id,version_no)؛ تغییرات immutable
CREATE TABLE IF NOT EXISTS control.config_revisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "config_id" TEXT,
  "version_no" INTEGER,
  "scope" TEXT,
  "value_json" JSONB,
  "changed_by" TEXT,
  "effective_at" TIMESTAMPTZ
);
CREATE SCHEMA IF NOT EXISTS control;
-- P02 | UNIQUE(switch_key,scope)؛ پیش از side effect خوانده شود
CREATE TABLE IF NOT EXISTS control.output_switches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "switch_key" TEXT,
  "scope" TEXT,
  "enabled" BOOLEAN,
  "revision" INTEGER,
  "updated_by" TEXT,
  "updated_at" TIMESTAMPTZ
);
CREATE SCHEMA IF NOT EXISTS control;
-- P02/P10 | نسخه‌بندی و ارجاع به قواعد، بدون تغییر متن منبع
CREATE TABLE IF NOT EXISTS control.editorial_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "rule_id" TEXT,
  "revision" INTEGER,
  "desk" TEXT,
  "kind" TEXT,
  "rule_json" JSONB,
  "approved_by" TEXT
);
CREATE SCHEMA IF NOT EXISTS sources;
-- P03 | UNIQUE(stream,url_normalized)؛ API keys فقط credential_ref
CREATE TABLE IF NOT EXISTS sources.source_registry (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "source_id" TEXT,
  "country" TEXT,
  "stream" TEXT,
  "url" TEXT,
  "mode" TEXT,
  "language" TEXT,
  "rights_scope" TEXT,
  "state" TEXT
);
CREATE INDEX IF NOT EXISTS ix_sources_source_registry_source_id ON sources.source_registry ("source_id");
CREATE INDEX IF NOT EXISTS ix_sources_source_registry_stream ON sources.source_registry ("stream");
CREATE SCHEMA IF NOT EXISTS identity;
-- P28 | سقف ۱۰ حساب انسانی فعال؛ گذرواژه هش‌شده؛ مجوز مدیریت کاربران
CREATE TABLE IF NOT EXISTS identity.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "user_id" TEXT,
  "username" TEXT,
  "role_id" TEXT,
  "password_hash" TEXT,
  "must_reset" BOOLEAN,
  "is_active" BOOLEAN
);
CREATE INDEX IF NOT EXISTS ix_identity_users_user_id ON identity.users ("user_id");
CREATE INDEX IF NOT EXISTS ix_identity_users_created_at ON identity.users ("created_at");
CREATE SCHEMA IF NOT EXISTS identity;
-- P28 | کلید(role_id,permission_key,resource_scope)
CREATE TABLE IF NOT EXISTS identity.roles_permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "role_id" TEXT,
  "permission_key" TEXT,
  "resource_scope" TEXT,
  "condition_json" JSONB
);
CREATE SCHEMA IF NOT EXISTS identity;
-- P28 | جلسه کوتاه‌عمر + MFA نقش ممتاز؛ audit
CREATE TABLE IF NOT EXISTS identity.auth_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "session_id" TEXT,
  "user_id" TEXT,
  "expires_at" TIMESTAMPTZ,
  "revoked_at" TIMESTAMPTZ,
  "client_fingerprint" TEXT
);
CREATE INDEX IF NOT EXISTS ix_identity_auth_sessions_user_id ON identity.auth_sessions ("user_id");
CREATE SCHEMA IF NOT EXISTS archive;
-- P26 | UNIQUE(news_id)؛ شاخص(stream,published_at)؛ متن منبع immutable
CREATE TABLE IF NOT EXISTS archive.news_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "news_id" TEXT,
  "stream" TEXT,
  "source_id" TEXT,
  "title" TEXT,
  "source_ref" TEXT,
  "published_at" TIMESTAMPTZ,
  "received_at" TIMESTAMPTZ,
  "classification" TEXT
);
CREATE INDEX IF NOT EXISTS ix_archive_news_records_news_id ON archive.news_records ("news_id");
CREATE INDEX IF NOT EXISTS ix_archive_news_records_source_id ON archive.news_records ("source_id");
CREATE INDEX IF NOT EXISTS ix_archive_news_records_stream ON archive.news_records ("stream");
CREATE SCHEMA IF NOT EXISTS archive;
-- P26 | صرفاً URI امن؛ فایل بزرگ در Object Store
CREATE TABLE IF NOT EXISTS archive.artifact_index (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "artifact_id" TEXT,
  "object_type" TEXT,
  "owner_project" TEXT,
  "object_uri" TEXT,
  "sha256" TEXT,
  "visibility" TEXT
);
CREATE INDEX IF NOT EXISTS ix_archive_artifact_index_created_at ON archive.artifact_index ("created_at");
CREATE SCHEMA IF NOT EXISTS orchestration;
-- P29 | UNIQUE(project_id,idempotency_key)؛ retry bounded
CREATE TABLE IF NOT EXISTS orchestration.jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "job_id" TEXT,
  "type" TEXT,
  "project_id" TEXT,
  "state" TEXT,
  "idempotency_key" TEXT,
  "attempts" INTEGER,
  "deadline_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ix_orchestration_jobs_job_id ON orchestration.jobs ("job_id");
CREATE SCHEMA IF NOT EXISTS orchestration;
-- P29 | Transactional Outbox و نگهداری محدود
CREATE TABLE IF NOT EXISTS orchestration.outbox (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "event_id" TEXT,
  "topic" TEXT,
  "aggregate_id" TEXT,
  "payload_ref" TEXT,
  "published_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ix_orchestration_outbox_created_at ON orchestration.outbox ("created_at");
CREATE SCHEMA IF NOT EXISTS security;
-- P28 | append-only؛ پاک‌کردن توسط نقش عملیاتی ممنوع
CREATE TABLE IF NOT EXISTS security.audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "audit_id" TEXT,
  "actor_id" TEXT,
  "action" TEXT,
  "object_type" TEXT,
  "object_id" TEXT,
  "time" TEXT,
  "reason" TEXT
);
CREATE SCHEMA IF NOT EXISTS processing;
-- P07 | source immutable, version of extraction recorded
CREATE TABLE IF NOT EXISTS processing.normalized_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "news_id" TEXT,
  "raw_ref" TEXT,
  "title" TEXT,
  "body_ref" TEXT,
  "lang" TEXT,
  "source_country" TEXT,
  "subject_countries" TEXT[],
  "quality" TEXT
);
CREATE INDEX IF NOT EXISTS ix_processing_normalized_items_news_id ON processing.normalized_items ("news_id");
CREATE SCHEMA IF NOT EXISTS processing;
-- P08 | نگه‌داشت منابع متعارض به‌صورت مستقل
CREATE TABLE IF NOT EXISTS processing.clusters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "cluster_id" TEXT,
  "canonical_id" TEXT,
  "similarity_version" INTEGER,
  "updated_at" TIMESTAMPTZ
);
CREATE SCHEMA IF NOT EXISTS processing;
-- P08 | UNIQUE(cluster_id,news_id)
CREATE TABLE IF NOT EXISTS processing.cluster_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "cluster_id" TEXT,
  "news_id" TEXT,
  "score" NUMERIC(7,4),
  "relation" TEXT
);
CREATE INDEX IF NOT EXISTS ix_processing_cluster_members_news_id ON processing.cluster_members ("news_id");
CREATE SCHEMA IF NOT EXISTS processing;
-- P09 | UNIQUE(news_id,desk_id)؛ سیاست داخلی/خارجی مستقل
CREATE TABLE IF NOT EXISTS processing.news_desks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "news_id" TEXT,
  "desk_id" TEXT,
  "priority_reason" TEXT,
  "version" INTEGER,
  "selected" BOOLEAN
);
CREATE INDEX IF NOT EXISTS ix_processing_news_desks_news_id ON processing.news_desks ("news_id");
CREATE SCHEMA IF NOT EXISTS editorial;
-- P10 | نقل‌قول‌ها هرگز auto_replace نشوند
CREATE TABLE IF NOT EXISTS editorial.rulesets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "ruleset_id" TEXT,
  "revision" INTEGER,
  "locale" TEXT,
  "desk" TEXT,
  "terms_ref" TEXT,
  "policy_ref" TEXT,
  "approved_at" TIMESTAMPTZ
);
CREATE SCHEMA IF NOT EXISTS editorial;
-- P11 | UNIQUE(object_id,policy_revision,content_hash)
CREATE TABLE IF NOT EXISTS editorial.policy_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "decision_id" TEXT,
  "object_id" TEXT,
  "decision" TEXT,
  "reasons_json" JSONB,
  "policy_revision" TEXT,
  "decided_at" TIMESTAMPTZ
);
CREATE SCHEMA IF NOT EXISTS editorial;
-- P12 | نگهداری متن اصلی و ارجاع ترجمه
CREATE TABLE IF NOT EXISTS editorial.translations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "translation_id" TEXT,
  "news_id" TEXT,
  "input_hash" TEXT,
  "lang_pair" TEXT,
  "model_ref" TEXT,
  "text_ref" TEXT,
  "qa_json" JSONB
);
CREATE INDEX IF NOT EXISTS ix_editorial_translations_news_id ON editorial.translations ("news_id");
CREATE SCHEMA IF NOT EXISTS editorial;
-- P13 | UNIQUE(article_id,version)؛ revisionهای غیرقابل ویرایش
CREATE TABLE IF NOT EXISTS editorial.articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "article_id" TEXT,
  "news_id" TEXT,
  "desk_id" TEXT,
  "version" INTEGER,
  "content_ref" TEXT,
  "summary_ref" TEXT,
  "state" TEXT
);
CREATE INDEX IF NOT EXISTS ix_editorial_articles_news_id ON editorial.articles ("news_id");
CREATE SCHEMA IF NOT EXISTS editorial;
-- P14 | حفظ حقوق تصویر و منشأ AI
CREATE TABLE IF NOT EXISTS editorial.image_assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "image_id" TEXT,
  "article_id" TEXT,
  "media_ref" TEXT,
  "rights_ref" TEXT,
  "rendition_json" JSONB,
  "approval" TEXT
);
CREATE SCHEMA IF NOT EXISTS insights;
-- P15 | اسناد/نقل‌قول‌ها و فرضیه جدا
CREATE TABLE IF NOT EXISTS insights.analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "analysis_id" TEXT,
  "topic" TEXT,
  "period_start" TEXT,
  "period_end" TEXT,
  "evidence_ref" TEXT,
  "confidence_note" TEXT
);
CREATE SCHEMA IF NOT EXISTS insights;
-- P16 | RLS/RBAC قبل از retrieval
CREATE TABLE IF NOT EXISTS insights.chat_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "chat_id" TEXT,
  "user_id" TEXT,
  "scope" TEXT,
  "started_at" TIMESTAMPTZ,
  "state" TEXT
);
CREATE INDEX IF NOT EXISTS ix_insights_chat_sessions_user_id ON insights.chat_sessions ("user_id");
CREATE SCHEMA IF NOT EXISTS insights;
-- P16 | داده محرمانه بدون دسترسی در prompt نیست
CREATE TABLE IF NOT EXISTS insights.chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "message_id" TEXT,
  "chat_id" TEXT,
  "actor" TEXT,
  "text_ref" TEXT,
  "evidence_ref" TEXT
);
CREATE INDEX IF NOT EXISTS ix_insights_chat_messages_created_at ON insights.chat_messages ("created_at");
CREATE SCHEMA IF NOT EXISTS insights;
-- P17 | UNIQUE(stream,desk,metric_date,snapshot_type)
CREATE TABLE IF NOT EXISTS insights.metric_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "snapshot_id" TEXT,
  "stream" TEXT,
  "desk" TEXT,
  "metric_date" DATE,
  "value_json" JSONB,
  "data_cutoff" TEXT
);
CREATE INDEX IF NOT EXISTS ix_insights_metric_snapshots_stream ON insights.metric_snapshots ("stream");
CREATE SCHEMA IF NOT EXISTS insights;
-- P18 | UNIQUE(report_day,report_slot,revision)؛ slot 1..4
CREATE TABLE IF NOT EXISTS insights.public_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "report_id" TEXT,
  "report_slot" INTEGER,
  "report_day" DATE,
  "revision" INTEGER,
  "content_ref" TEXT,
  "validation_state" TEXT
);
CREATE INDEX IF NOT EXISTS ix_insights_public_reports_report_day ON insights.public_reports ("report_day");
CREATE SCHEMA IF NOT EXISTS executive;
-- P19 | slot 5..7؛ DB role و bucket خصوصی؛ publishable=false
CREATE TABLE IF NOT EXISTS executive.private_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "report_id" TEXT,
  "report_slot" INTEGER,
  "report_day" DATE,
  "content_ref" TEXT,
  "owner_id" TEXT,
  "restricted_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ix_executive_private_reports_report_day ON executive.private_reports ("report_day");
CREATE SCHEMA IF NOT EXISTS studio;
-- P20 | اطلاعات صدای مجاز و متن خوانده‌شده
CREATE TABLE IF NOT EXISTS studio.audio_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "audio_id" TEXT,
  "article_id" TEXT,
  "text_hash" TEXT,
  "voice_ref" TEXT,
  "artifact_ref" TEXT,
  "review_state" TEXT
);
CREATE SCHEMA IF NOT EXISTS studio;
-- P21 | ثبت هویت مجری مصنوعی و watermark
CREATE TABLE IF NOT EXISTS studio.video_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "video_id" TEXT,
  "audio_id" TEXT,
  "avatar_ref" TEXT,
  "scene_ref" TEXT,
  "artifact_ref" TEXT,
  "synthetic_label" BOOLEAN
);
CREATE SCHEMA IF NOT EXISTS publish;
-- P23 | UNIQUE(provider,channel_ref)؛ credential امن و مجوز تست‌شده
CREATE TABLE IF NOT EXISTS publish.destinations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "destination_id" TEXT,
  "provider" TEXT,
  "channel_ref" TEXT,
  "stream" TEXT,
  "desk" TEXT,
  "credential_ref" TEXT,
  "verified" BOOLEAN
);
CREATE INDEX IF NOT EXISTS ix_publish_destinations_stream ON publish.destinations ("stream");
CREATE SCHEMA IF NOT EXISTS publish;
-- P22 | UNIQUE(publication_intent_key)؛ تاریخ انقضا
CREATE TABLE IF NOT EXISTS publish.jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "job_id" TEXT,
  "article_id" TEXT,
  "report_id" TEXT,
  "stream" TEXT,
  "deadline_at" TIMESTAMPTZ,
  "schedule_at" TIMESTAMPTZ,
  "state" TEXT,
  "policy_decision_id" TEXT
);
CREATE INDEX IF NOT EXISTS ix_publish_jobs_schedule_at ON publish.jobs ("schedule_at");
CREATE INDEX IF NOT EXISTS ix_publish_jobs_job_id ON publish.jobs ("job_id");
CREATE INDEX IF NOT EXISTS ix_publish_jobs_stream ON publish.jobs ("stream");
CREATE SCHEMA IF NOT EXISTS publish;
-- P24 | UNIQUE(job_id,destination_id)؛ rendition سازگار
CREATE TABLE IF NOT EXISTS publish.payloads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "payload_id" TEXT,
  "job_id" TEXT,
  "destination_id" TEXT,
  "message_ref" TEXT,
  "image_ref" TEXT,
  "payload_hash" TEXT
);
CREATE INDEX IF NOT EXISTS ix_publish_payloads_job_id ON publish.payloads ("job_id");
CREATE SCHEMA IF NOT EXISTS publish;
-- P25 | UNIQUE(job_id,destination_id,attempt_no)؛ وضعیت unknown مهار شود
CREATE TABLE IF NOT EXISTS publish.attempts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "attempt_id" TEXT,
  "job_id" TEXT,
  "destination_id" TEXT,
  "status" TEXT,
  "provider_msg_id" TEXT,
  "started_at" TIMESTAMPTZ,
  "ended_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ix_publish_attempts_job_id ON publish.attempts ("job_id");
CREATE SCHEMA IF NOT EXISTS ui;
-- P27 | dashboard_type owner/editor_in_chief/staff
CREATE TABLE IF NOT EXISTS ui.saved_views (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "view_id" TEXT,
  "user_id" TEXT,
  "dashboard_type" TEXT,
  "filters_json" JSONB
);
CREATE INDEX IF NOT EXISTS ix_ui_saved_views_user_id ON ui.saved_views ("user_id");
CREATE INDEX IF NOT EXISTS ix_ui_saved_views_created_at ON ui.saved_views ("created_at");
CREATE SCHEMA IF NOT EXISTS ui;
-- P27 | مالکیت preference نزد UI؛ حق دسترسی نزد P28
CREATE TABLE IF NOT EXISTS ui.notification_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  "user_id" TEXT,
  "scope" TEXT,
  "channels_json" JSONB,
  "enabled" BOOLEAN
);
CREATE INDEX IF NOT EXISTS ix_ui_notification_preferences_user_id ON ui.notification_preferences ("user_id");
-- Optional hardening rules/indices to convert into reviewed migrations:
CREATE UNIQUE INDEX IF NOT EXISTS ux_output_switches_scope ON control.output_switches (switch_key, scope);
CREATE UNIQUE INDEX IF NOT EXISTS ux_source_registry_stream_url ON sources.source_registry (stream, url);
CREATE UNIQUE INDEX IF NOT EXISTS ux_identity_users_username ON identity.users (username);
CREATE UNIQUE INDEX IF NOT EXISTS ux_orchestration_jobs_idempotency ON orchestration.jobs (project_id, idempotency_key);
CREATE UNIQUE INDEX IF NOT EXISTS ux_publish_payloads_dest ON publish.payloads (job_id, destination_id);
CREATE UNIQUE INDEX IF NOT EXISTS ux_publish_attempts_provider_msg ON publish.attempts (destination_id, provider_msg_id) WHERE provider_msg_id IS NOT NULL;
ALTER TABLE executive.private_reports ADD CONSTRAINT private_slot_only CHECK (report_slot BETWEEN 5 AND 7);
ALTER TABLE insights.public_reports ADD CONSTRAINT public_slot_only CHECK (report_slot BETWEEN 1 AND 4);
-- TODO SECURITY: configure RLS for private_reports, separate DB role and object bucket.
-- TODO CAP: enforce active human user <=10 inside single serialized transaction; advisory lock.
-- TODO PASSWORD: user.password_hash is Argon2id output, not credentials; first-login reset mandatory.
-- TODO MIGRATION: apply owner-specific GRANT; prohibit direct DB access between services.
