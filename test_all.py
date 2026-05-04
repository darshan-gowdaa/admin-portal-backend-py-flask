import urllib.request
import urllib.error
import json
import http.cookiejar
import sqlite3

BASE = 'http://127.0.0.1:5000'
PASS = []
FAIL = []


def make_session():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def req(opener, method, path, body=None, expect_status=None, label=''):
    url = BASE + path
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(
        url, data=data, method=method,
        headers={'Content-Type': 'application/json'} if data else {},
    )
    try:
        resp = opener.open(r)
        status = resp.status
        try:
            text = json.loads(resp.read())
        except Exception:
            text = {}
    except urllib.error.HTTPError as e:
        status = e.status
        try:
            text = json.loads(e.read())
        except Exception:
            text = {}
    ok = (status == expect_status) if expect_status is not None else True
    tag = '[PASS]' if ok else '[FAIL]'
    (PASS if ok else FAIL).append(label)
    print(f'{tag} {label} -> HTTP {status} | {text}')
    return status, text


def check(condition, label):
    tag = '[PASS]' if condition else '[FAIL]'
    (PASS if condition else FAIL).append(label)
    print(f'{tag} {label}')


# ===========================================================
print('=== AUTH — SIGNUP ===')
s = make_session()
req(s, 'POST', '/auth/signup', {
    'full_name': 'Full Test', 'email': 'fulltest2@qf.org.qa',
    'password': 'Secure123!', 'confirm_password': 'Secure123!'
}, 201, 'signup - success')
req(s, 'POST', '/auth/signup', {
    'full_name': 'Full Test', 'email': 'fulltest2@qf.org.qa',
    'password': 'Secure123!', 'confirm_password': 'Secure123!'
}, 409, 'signup - duplicate email')
req(s, 'POST', '/auth/signup', {
    'full_name': '', 'email': 'a@b.com',
    'password': 'Secure123!', 'confirm_password': 'Secure123!'
}, 400, 'signup - missing full name')
req(s, 'POST', '/auth/signup', {
    'full_name': 'X', 'email': 'notanemail',
    'password': 'Secure123!', 'confirm_password': 'Secure123!'
}, 400, 'signup - invalid email')
req(s, 'POST', '/auth/signup', {
    'full_name': 'X', 'email': 'new@b.com',
    'password': 'short', 'confirm_password': 'short'
}, 400, 'signup - password too short')
req(s, 'POST', '/auth/signup', {
    'full_name': 'X', 'email': 'new2@b.com',
    'password': 'Secure123!', 'confirm_password': 'Different!'
}, 400, 'signup - passwords mismatch')

# ===========================================================
print('\n=== AUTH — LOGIN ===')
req(s, 'POST', '/auth/login', {
    'email': 'fulltest2@qf.org.qa', 'password': 'Secure123!'
}, 200, 'login - success')
req(s, 'POST', '/auth/login', {
    'email': 'fulltest2@qf.org.qa', 'password': 'wrongpass'
}, 401, 'login - wrong password')
req(s, 'POST', '/auth/login', {
    'email': 'ghost@qf.org.qa', 'password': 'Secure123!'
}, 401, 'login - nonexistent user (generic error)')

# ===========================================================
print('\n=== AUTH — FORGOT PASSWORD ===')
_, fp1 = req(s, 'POST', '/auth/forgot-password', {
    'email': 'fulltest2@qf.org.qa'
}, 200, 'forgot-password - registered email')
check('reset link' in fp1.get('message', '').lower(), 'forgot-password - correct message')

_, fp2 = req(s, 'POST', '/auth/forgot-password', {
    'email': 'nobody@fake.com'
}, 200, 'forgot-password - unregistered (privacy: always 200)')
check(fp1.get('message') == fp2.get('message'), 'forgot-password - same message regardless of email')

# ===========================================================
print('\n=== OPPORTUNITIES — CRUD ===')
req(s, 'GET', '/api/opportunities/', None, 200, 'GET opportunities - logged in')

_, created = req(s, 'POST', '/api/opportunities/', {
    'name': 'AI Internship', 'category': 'Technology', 'duration': '3 months',
    'start_date': '2025-09-01', 'description': 'Work on AI projects',
    'skills_to_gain': 'Python,ML,TensorFlow', 'future_opportunities': 'Full-time role',
    'max_applicants': '50',
}, 201, 'create opportunity - success')
opp_id = created.get('id')

req(s, 'POST', '/api/opportunities/', {
    'name': 'Missing Dur', 'category': 'Design', 'duration': '',
    'start_date': '2025-01-01', 'description': 'desc',
    'skills_to_gain': 'skill', 'future_opportunities': 'future',
}, 400, 'create - missing duration (400)')
req(s, 'POST', '/api/opportunities/', {
    'name': 'Bad Cat', 'category': 'INVALID', 'duration': '1 month',
    'start_date': '2025-01-01', 'description': 'desc',
    'skills_to_gain': 'skill', 'future_opportunities': 'future',
}, 400, 'create - invalid category (400)')
req(s, 'POST', '/api/opportunities/', {
    'name': 'Bad Max', 'category': 'Other', 'duration': '1 month',
    'start_date': '2025-01-01', 'description': 'desc',
    'skills_to_gain': 'skill', 'future_opportunities': 'future',
    'max_applicants': '-5',
}, 400, 'create - negative max_applicants (400)')

req(s, 'GET', f'/api/opportunities/{opp_id}', None, 200, 'GET single opportunity')
req(s, 'GET', '/api/opportunities/99999', None, 404, 'GET non-existent opportunity (404)')

req(s, 'PUT', f'/api/opportunities/{opp_id}', {
    'name': 'AI Internship UPDATED', 'category': 'Data Science', 'duration': '6 months',
    'start_date': '2025-10-01', 'description': 'Updated description',
    'skills_to_gain': 'Python,ML', 'future_opportunities': 'Senior role',
}, 200, 'PUT update opportunity')

req(s, 'DELETE', f'/api/opportunities/{opp_id}', None, 200, 'DELETE opportunity')
req(s, 'GET', f'/api/opportunities/{opp_id}', None, 404, 'GET after delete (404)')

# ===========================================================
print('\n=== CROSS-ADMIN ISOLATION ===')
a = make_session()
b = make_session()
req(a, 'POST', '/auth/signup', {
    'full_name': 'Admin A', 'email': 'adminA2@qf.org.qa',
    'password': 'PasswordA1!', 'confirm_password': 'PasswordA1!'
}, 201, 'create admin A')
req(b, 'POST', '/auth/signup', {
    'full_name': 'Admin B', 'email': 'adminB2@qf.org.qa',
    'password': 'PasswordB1!', 'confirm_password': 'PasswordB1!'
}, 201, 'create admin B')
req(a, 'POST', '/auth/login', {'email': 'adminA2@qf.org.qa', 'password': 'PasswordA1!'}, 200, 'login admin A')
req(b, 'POST', '/auth/login', {'email': 'adminB2@qf.org.qa', 'password': 'PasswordB1!'}, 200, 'login admin B')

_, opp_a = req(a, 'POST', '/api/opportunities/', {
    'name': 'Admin A Only', 'category': 'Business', 'duration': '2 months',
    'start_date': '2025-06-01', 'description': 'A-only',
    'skills_to_gain': 'Management', 'future_opportunities': 'Leadership',
}, 201, 'admin A creates opportunity')
oid = opp_a.get('id')

req(a, 'GET', f'/api/opportunities/{oid}', None, 200, 'admin A reads own opportunity (200)')
req(b, 'GET', f'/api/opportunities/{oid}', None, 403, 'admin B reads admin A opp (must 403)')
req(b, 'PUT', f'/api/opportunities/{oid}', {
    'name': 'Hacked', 'category': 'Other', 'duration': '1 month',
    'start_date': '2025-01-01', 'description': 'hacked',
    'skills_to_gain': 'hacking', 'future_opportunities': 'evil',
}, 403, 'admin B updates admin A opp (must 403)')
req(b, 'DELETE', f'/api/opportunities/{oid}', None, 403, 'admin B deletes admin A opp (must 403)')

_, b_list = req(b, 'GET', '/api/opportunities/', None, 200, 'admin B list (sees 0)')
check(len(b_list) == 0, 'admin B sees zero opportunities (data isolated)')

# ===========================================================
print('\n=== PASSWORD RESET FULL FLOW ===')
c = make_session()
req(c, 'POST', '/auth/signup', {
    'full_name': 'Reset Test', 'email': 'resetme2@qf.org.qa',
    'password': 'OldPass123!', 'confirm_password': 'OldPass123!'
}, 201, 'create reset-test admin')
req(c, 'POST', '/auth/forgot-password', {'email': 'resetme2@qf.org.qa'}, 200, 'trigger forgot-password')

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('SELECT token FROM password_reset_tokens ORDER BY id DESC LIMIT 1')
row = cur.fetchone()
conn.close()
token = row[0] if row else None
check(token is not None, 'reset token saved to DB')

if token:
    req(c, 'GET', f'/auth/reset-password/{token}', None, 200, 'GET reset-password - valid token (200)')
    req(c, 'POST', f'/auth/reset-password/{token}', {'password': 'NewPass456!'}, 200, 'POST reset-password - set new password')
    req(c, 'POST', f'/auth/reset-password/{token}', {'password': 'Another789!'}, 400, 'POST reset-password - token reuse (must 400)')
    req(c, 'POST', '/auth/login', {'email': 'resetme2@qf.org.qa', 'password': 'NewPass456!'}, 200, 'login with NEW password')
    req(c, 'POST', '/auth/login', {'email': 'resetme2@qf.org.qa', 'password': 'OldPass123!'}, 401, 'login with OLD password (must 401)')

# ===========================================================
print('\n=== LOGOUT + POST-LOGOUT PROTECTION ===')
req(s, 'POST', '/auth/logout', {}, 200, 'logout')
req(s, 'GET', '/api/opportunities/', None, 401, 'GET opportunities after logout (must 401)')
req(s, 'POST', '/api/opportunities/', {
    'name': 'X', 'category': 'Other', 'duration': '1 month',
    'start_date': '2025-01-01', 'description': 'x',
    'skills_to_gain': 'x', 'future_opportunities': 'x',
}, 401, 'POST opportunity after logout (must 401)')

# ===========================================================
print('\n=== STATIC FILES ===')
d = make_session()
status, _ = req(d, 'GET', '/', None, 200, 'GET / (admin.html)')
req(d, 'GET', '/admin.css', None, 200, 'GET /admin.css')
req(d, 'GET', '/admin.js', None, 200, 'GET /admin.js')

# ===========================================================
print()
print(f'=== FINAL RESULTS: {len(PASS)} passed, {len(FAIL)} failed ===')
if FAIL:
    print('FAILED TESTS:')
    for f in FAIL:
        print(f'  - {f}')
else:
    print('ALL TESTS PASSED')
