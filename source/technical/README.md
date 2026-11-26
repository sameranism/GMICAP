# اتاق خبر هوشمند اعتماد | ضمائم معماری v1.1

این پوشه **سند طراحی و مرجع تیم‌های توسعه** است؛ سرویس اجرایی، دیتابیس عملیاتی و رمز کاربری ندارد.

- `project_package_map.csv`: انتساب ثابت P01–P29 به B01–B09
- `database_dictionary.csv`: فهرست پیشنهادی جدول‌ها و مالکیت داده
- `architecture_packages.json`: تصمیم‌های معماری نسخه ۱.۱
- `dependency_edges.csv`: ارتباطات مبنای قبلی
- `example_event.json`: نمونه پاکت رویداد
- `postgres_central_schema_PROPOSAL.sql`, `postgres_domestic_schema_PROPOSAL.sql`, `postgres_foreign_schema_PROPOSAL.sql`: پیشنهاد DDL تایپ‌شده در ۳ محیط مجزا؛ هنوز migration تأییدشده تولید نیست
- `data_flows.mmd`: نمودار Mermaid جریان‌ها
- قراردادهای ۳۰گانه نسخه پیشین در `baseline_contracts/` همراه بسته هستند و بدون مهاجرت تغییر داده نمی‌شوند.

ملاک پیاده‌سازی، نسخه قفل‌شده قرارداد در مخزن است. متن اسناد حقوقی تنها مرجع ارزیابی اولیه‌اند؛ تطبیق قانونی باید با مسئول حقوقی رسانه انجام شود.
