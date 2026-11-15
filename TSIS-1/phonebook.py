"""TSIS1 extension to Practice 7/8 PhoneBook; PostgreSQL-backed CLI."""
import csv
import json
from datetime import date
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
from connect import get_connection

ROOT = Path(__file__).resolve().parent
VALID_TYPES = ('home', 'work', 'mobile')
SORTS = {'name': 'c.name ASC', 'birthday': 'c.birthday ASC NULLS LAST', 'date': 'c.created_at DESC'}


def setup():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute((ROOT / 'schema.sql').read_text())
            cur.execute((ROOT / 'procedures.sql').read_text())
    print('Database schema and procedures ready.')


def fetch(query, params=()):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]


def show(rows):
    if not rows:
        print('No contacts found.')
        return
    for c in rows:
        phones = c.get('phones') or []
        if isinstance(phones, str):
            phones = json.loads(phones)
        phone_text = ', '.join(f"{p['phone']} ({p['type']})" for p in phones)
        print(f"{c['id']}: {c['name']} {c.get('surname') or ''} | {c.get('email') or '-'} | "
              f"{c.get('birthday') or '-'} | {c.get('group_name') or '-'} | {phone_text or '-'}")


BASE = """SELECT c.id,c.name,c.surname,c.email,c.birthday,c.created_at,
 g.name AS group_name,
 COALESCE((SELECT json_agg(json_build_object('phone',p.phone,'type',p.type) ORDER BY p.id)
 FROM phones p WHERE p.contact_id=c.id),'[]'::json) AS phones
 FROM contacts c LEFT JOIN groups g ON g.id=c.group_id"""


def list_contacts(group=None, email=None, sort='name', limit=None, offset=0):
    where, args = [], []
    if group:
        where.append('g.name ILIKE %s')
        args.append(group)
    if email:
        where.append('c.email ILIKE %s')
        args.append('%'+email+'%')
    query = BASE + (' WHERE ' + ' AND '.join(where) if where else '')
    query += ' ORDER BY ' + SORTS.get(sort, SORTS['name']) + ', c.id'
    if limit is not None:
        query += ' LIMIT %s OFFSET %s'
        args += [limit, offset]
    return fetch(query, tuple(args))


def search():
    query = input('Search name, surname, email or any phone: ').strip()
    rows = fetch('SELECT id FROM search_contacts(%s)', (query,))
    ids = [r['id'] for r in rows]
    if not ids:
        show([])
    else:
        show(fetch(BASE + ' WHERE c.id = ANY(%s) ORDER BY c.name', (ids,)))


def validate_birthday(value):
    if not value:
        return None
    return date.fromisoformat(str(value)).isoformat()


def save_contact(data, overwrite=False):
    name = str(data.get('name') or '').strip()
    if not name:
        raise ValueError('Contact name is required')
    surname = str(data.get('surname') or '').strip()
    email = str(data.get('email') or '').strip() or None
    birthday = validate_birthday(data.get('birthday'))
    group = str(data.get('group') or data.get('group_name') or 'Other').strip() or 'Other'
    phones = data.get('phones') or []
    if isinstance(phones, str):
        phones = json.loads(phones)
    if not phones and data.get('phone'):
        phones = [{'phone': data['phone'], 'type': data.get('phone_type') or 'mobile'}]
    if not isinstance(phones, list):
        raise ValueError('phones must be a list')
    for p in phones:
        if p.get('type') not in VALID_TYPES:
            raise ValueError('Phone type must be home, work or mobile')
        phone = str(p.get('phone') or '')
        if not (phone.lstrip('+').isdigit() and 10 <= len(phone.lstrip('+')) <= 15 and phone.count('+') <= 1 and (not '+' in phone or phone.startswith('+'))):
            raise ValueError('Invalid phone: ' + phone)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM contacts WHERE name=%s FOR UPDATE', (name,))
            found = cur.fetchone()
            if found and not overwrite:
                return False
            cur.execute('INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING', (group,))
            cur.execute('SELECT id FROM groups WHERE name=%s', (group,))
            group_id = cur.fetchone()[0]
            first_phone = str(phones[0]['phone']) if phones else ''
            if found:
                contact_id = found[0]
                cur.execute('UPDATE contacts SET surname=%s,phone=%s,email=%s,birthday=%s,group_id=%s WHERE id=%s',
                            (surname,first_phone,email,birthday,group_id,contact_id))
                cur.execute('DELETE FROM phones WHERE contact_id=%s', (contact_id,))
            else:
                cur.execute('INSERT INTO contacts(name,surname,phone,email,birthday,group_id) VALUES(%s,%s,%s,%s,%s,%s) RETURNING id',
                            (name,surname,first_phone,email,birthday,group_id))
                contact_id = cur.fetchone()[0]
            for p in phones:
                cur.execute('INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s) ON CONFLICT(contact_id,phone) DO UPDATE SET type=EXCLUDED.type',
                            (contact_id,str(p['phone']),p['type']))
    return True


def add_contact():
    data = {k: input(k + ': ').strip() for k in ('name','surname','email','birthday','group')}
    data['phones'] = []
    while True:
        phone = input('Phone (blank to finish): ').strip()
        if not phone:
            break
        typ = input('Type (home/work/mobile): ').strip().lower()
        data['phones'].append({'phone':phone,'type':typ})
    ok = save_contact(data)
    print('Saved.' if ok else 'Name already exists.')


def export_json():
    target = Path(input('Output JSON file [contacts_export.json]: ').strip() or 'contacts_export.json')
    rows = list_contacts()
    for row in rows:
        row.pop('id',None)
        row.pop('created_at',None)
        if row.get('birthday'):
            row['birthday'] = row['birthday'].isoformat()
        row['group'] = row.pop('group_name')
    target.write_text(json.dumps(rows,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    print(f'Exported {len(rows)} contacts to {target}')


def import_items(items):
    imported = skipped = 0
    for item in items:
        try:
            ok = save_contact(item)
            if not ok:
                decision = input(f"Duplicate '{item.get('name')}'. [s]kip/[o]verwrite: ").strip().lower()
                if decision in ('o','overwrite'):
                    ok = save_contact(item,overwrite=True)
            if ok:
                imported += 1
            else:
                skipped += 1
        except (ValueError,psycopg2.Error) as exc:
            print(f"Skipped {item.get('name')}: {exc}")
            skipped += 1
    print(f'Imported: {imported}, skipped: {skipped}')


def import_json():
    path = Path(input('JSON path: ').strip())
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,list):
        raise ValueError('JSON must contain a list of contacts')
    import_items(data)


def import_csv():
    path = Path(input('CSV path [contacts.csv]: ').strip() or str(ROOT / 'contacts.csv'))
    with path.open(newline='',encoding='utf-8-sig') as f:
        items = list(csv.DictReader(f))
    # Multiple rows with the same name represent multiple phones for that contact.
    merged = {}
    for row in items:
        name = (row.get('name') or '').strip()
        if name not in merged:
            merged[name] = {k:row.get(k) for k in ('name','surname','email','birthday','group')}
            merged[name]['phones'] = []
        if row.get('phone'):
            merged[name]['phones'].append({'phone':row['phone'],'type':row.get('phone_type') or 'mobile'})
    import_items(list(merged.values()))


def paginate():
    page_size = 5
    page = 0
    while True:
        rows = list_contacts(sort='name',limit=page_size,offset=page*page_size)
        print(f'\nPage {page+1}')
        show(rows)
        command = input('[next / prev / quit]: ').strip().lower()
        if command == 'quit':
            break
        if command == 'next':
            if len(rows) < page_size or not list_contacts(sort='name',limit=1,offset=(page+1)*page_size):
                print('Last page.')
            else:
                page += 1
        elif command == 'prev':
            page = max(0,page-1)


def add_phone():
    name = input('Contact name: ').strip()
    phone = input('New phone: ').strip()
    typ = input('Type (home/work/mobile): ').strip().lower()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('CALL add_phone(%s::varchar,%s::varchar,%s::varchar)',(name,phone,typ))
    print('Phone added.')


def move_group():
    name = input('Contact name: ').strip()
    group = input('New group: ').strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('CALL move_to_group(%s::varchar,%s::varchar)',(name,group))
    print('Group updated.')


def main():
    menu = '''\nTSIS1 PhoneBook
1 Add contact
2 List / filter by group / search email / sort
3 Search all fields
4 Navigate pages (next/prev/quit)
5 Export JSON
6 Import JSON
7 Import CSV
8 Add phone (procedure)
9 Move to group (procedure)
0 Exit
Choice: '''
    actions = {'1':add_contact,'3':search,'4':paginate,'5':export_json,
               '6':import_json,'7':import_csv,'8':add_phone,'9':move_group}
    while True:
        choice = input(menu).strip()
        if choice == '0':
            break
        try:
            if choice == '2':
                group = input('Group (blank=all): ').strip() or None
                email = input('Email contains (blank=all): ').strip() or None
                sort = input('Sort name/birthday/date [name]: ').strip().lower() or 'name'
                show(list_contacts(group,email,sort))
            elif choice in actions:
                actions[choice]()
            else:
                print('Unknown choice.')
        except (OSError,ValueError,psycopg2.Error,json.JSONDecodeError) as exc:
            print('Error:',exc)

if __name__ == '__main__':
    try:
        setup()
        main()
    except psycopg2.Error as exc:
        print('Database connection/setup error:',exc)
        print('Check PostgreSQL and PGUSER/PGPASSWORD/PGDATABASE settings in README.md')
