# راه‌اندازی در Windows 11 + Cursor (PowerShell)

**پیش‌نیاز:** ZIP را با مسیر انتخابی خودت Extract کن. این راهنما هیچ تغییری در حساب/مخزن تو انجام نداده است.

```powershell
# در یک پوشه خصوصی و خالی، محتویات بسته پرامپت را استخراج کن:
Expand-Archive -Path .\ETEMAD_CURSOR_PROMPTS_STAGE0_TO_RELEASE_v2.zip -DestinationPath .\ETEMAD -Force
Set-Location .\ETEMAD
# از دستورهای زیر فقط در repo واقعی که قصد توسعه آن را داری استفاده کن:
Copy-Item .\cursor-kit\AGENTS.md .\AGENTS.md -Force
New-Item -ItemType Directory .\.cursor\rules -Force | Out-Null
Copy-Item .\cursor-kit\.cursor\rules\*.mdc .\.cursor\rules\ -Force
# حالا این پوشه را در Cursor باز کن و README_FA.md را بخوان.
```

**اگر مخزن کد قبلی داری:** این فایل‌ها را نخست در یک شاخه آزمایشی کپی کن و از `git diff` برای جلوگیری از بازنویسی استفاده کن. `git init` فقط در یک مخزن واقعاً خالی لازم است. برای Cloud باید مخزن به GitHub و Cloud Environment واقعی وصل شود؛ تنظیم اتصال، احراز هویت و مجوزها را خودت در Cursor انجام بده.

**تسک اول:** `prompts/00_BOOTSTRAP/SHARED/S00-001__AGENTS_md.md` را باز کن و بخش «پرامپت آماده» را به Codex بده.
