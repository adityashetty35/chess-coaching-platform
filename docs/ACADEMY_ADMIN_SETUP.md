# Academy administration, WhatsApp, OTP, audit

This change is local only; it has **not** been pushed to GitHub or deployed.

## Apply safely when ready

1. Back up the **existing** PythonAnywhere SQLite database. Do not replace, reset, flush, or seed it.
2. Deploy code without including an SQLite database file.
3. Run `python manage.py migrate` against the existing database. Migrations only add RBAC, integration, audit, and coach-assignment tables/columns.
4. Run `python manage.py check`, reload the web app, then verify the existing records remain intact.
5. Log in as an existing Django **superuser**; the Users & Roles, WhatsApp & OTP, Delivery Logs and Audit Logs links appear in the sidebar. Identify the correct owner's user before assigning or creating a personal Super Administrator login.

## Roles

- **Super Administrator:** an active Django `is_superuser` user. Can configure users, roles, academy information, WhatsApp, SMS OTP, logs, and all modules.
- **Academy Admin:** individually selected module permissions. Existing staff without an explicit role retain academy-admin capabilities for compatibility.
- **Coach:** only assigned lessons/attendance, student progress/test records tied to assigned lessons, global syllabus, and homework explicitly assigned to them. Administrators assign coaches when editing classes and homework.
- **Parent:** linked parent profile only. Link a parent record when creating/editing their Django user.

Role and permission changes are recorded as audit events. Fee record create/update/delete actions are audited from authenticated HTTP requests; academy contact changes and integration/schedule/template changes are audited too.

## WhatsApp (Twilio)

Environment variables (configure **on the server**, never in repository files):

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_VERIFY_SERVICE_SID` (only needed for OTP)

In Administration → WhatsApp & OTP:

1. Select **Twilio WhatsApp**, enter a provisioned approved WhatsApp sender.
2. Create one or more **approved WhatsApp Content templates** in Twilio and record their `HX…` SIDs in the **message templates** section. The template variables are fixed to: `{{1}}` parent name, `{{2}}` student, `{{3}}` outstanding amount, `{{4}}` due date. Match this order in Twilio's approved template.
3. Add reminder schedules, e.g. -3 days, 0 days, +2 days relative to an invoice due date. The existing single reminder-days setting is used only if no schedule records exist.
4. Enable reminders. Only unpaid invoices with parents preferring WhatsApp and having a WhatsApp number are eligible. An attempt is logged once per invoice, schedule and run date; provider acceptance is **not** equivalent to confirmed delivery.
5. Set a daily scheduled task in PythonAnywhere to run: `cd /home/<username>/chess-coaching-platform && python3.10 manage.py process_notifications` using the app's Python environment. This sends due reminders and queries Twilio for pending delivery status.

On PythonAnywhere free plans, outbound connectivity, scheduled task allowances, and WhatsApp provider requirements may restrict automatic sending. Verify this with a real authorized test number before enabling production reminders. The old manual wa.me flow remains available; opening it is no longer marked as delivered.

## Parent OTP

1. Configure a Twilio Verify Service, then `TWILIO_VERIFY_SERVICE_SID` on the server.
2. Set SMS provider to **Twilio Verify**, then enable **Parent OTP**.
3. Confirm a parent profile is linked to the correct **active** Django user and their phone includes E.164 country code (`+91…`). Duplicate phone numbers are rejected for OTP login rather than selecting the wrong account.
4. Parents can open `/accounts/parent-otp/`; Django still supports username/password login.

Verification is handled by Twilio Verify; no raw codes are stored locally. Request cooldown, IP throttling, a ten-minute request window, and per-request verification attempt limits are enforced. Parent OTP login is unavailable until configuration and credentials are valid.

## Validation

Run `PYTHONPATH=/tmp/chess-django-deps python manage.py test core progress` where the temporary local Django dependencies are installed, or `python manage.py test core progress` in your normal venv.

These features require provider provisioning and server-side scheduling before they will send real messages. No existing database records should be deleted or re-seeded.
