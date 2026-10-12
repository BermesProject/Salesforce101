import csv
import importlib.util
import json
import unittest
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = {'m': 'http://soap.sforce.com/2006/04/metadata'}


def rows(path):
    with (ROOT / path).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def schema(topic):
    return json.loads((ROOT / topic / 'schema.json').read_text())


class KitTests(unittest.TestCase):
    def test_employee_identity_and_xml(self):
        data = rows('Common/Data/employees.csv')
        by_key = {r['Employee_Number__c']: r for r in data}
        self.assertEqual(len(data), 6)
        self.assertEqual(len(by_key), 6)
        self.assertEqual(by_key['EMP-LUX-001']['Manager_Employee_Code'], 'EMP-LUX-002')
        self.assertEqual(by_key['EMP-LUX-002']['Name'], '미란다')
        self.assertEqual({r['Active__c'] for r in data}, {'true'})
        self.assertNotIn('우영', {r['Name'] for r in data})
        for field in schema('Common')['fields']:
            xml = ET.parse(ROOT / 'Common/Field' / (field['api'] + '.field.xml')).getroot()
            self.assertEqual(xml.findtext('m:fullName', namespaces=NS), field['api'])
            self.assertEqual(xml.findtext('m:type', namespaces=NS), field['type'])
            if field.get('unique'):
                self.assertEqual(xml.findtext('m:unique', namespaces=NS), 'true')
                self.assertEqual(xml.findtext('m:externalId', namespaces=NS), 'true')
        for p in (ROOT / 'Common').rglob('*.xml'):
            ET.parse(p)

    def test_csv_schema_mapping_and_values(self):
        mappings = {
            'Common': {'Manager_Employee_Code': 'Manager_Employee__c'},
            'Game': {'Campaign_Code': 'Campaign__c', 'Assigned_Employee_Code': 'Assigned_Employee__c'},
            'Eyewear': {'Advisor_Code': 'Advisor__c', 'Manager_Employee_Code': 'Manager_Employee__c', 'Current_Handler_Code': 'Current_Handler__c', 'Received_Offset_Hours': 'Received_At__c', 'Due_Offset_Hours': 'Response_Due_At__c', 'First_Response_Offset_Hours': 'First_Response_At__c'},
            'AI-Sales': {'Sales_Employee_Code': 'Sales_Employee__c', 'Technical_Employee_Code': 'Technical_Employee__c', 'Project_Coordinator_Code': 'Project_Coordinator__c'},
        }
        files = {'Common': 'employees.csv', 'Game': 'performance.csv', 'Eyewear': 'consultation-templates.csv', 'AI-Sales': 'projects.csv'}
        employees = {r['Employee_Number__c']: r for r in rows('Common/Data/employees.csv')}
        campaigns = {r['Training_Campaign_Code__c'] for r in rows('Game/Data/campaigns.csv')}
        for topic, filename in files.items():
            fields = {f['api']: f for f in schema(topic)['fields']}
            if topic == 'Common':
                fields['Name'] = {'type': 'Text', 'length': 80}
            for row in rows(f'{topic}/Data/{filename}'):
                for col, val in row.items():
                    target = mappings[topic].get(col, col)
                    self.assertIn(target, fields, f'{topic}: {col}')
                    f = fields[target]
                    if not val:
                        continue
                    if col.endswith('_Code'):
                        self.assertIn(val, campaigns if col == 'Campaign_Code' else employees)
                    elif col.endswith('_Offset_Hours'):
                        float(val)
                    elif f['type'] == 'Picklist':
                        self.assertIn(val, [x['value'] if isinstance(x, dict) else x for x in f['values']])
                    elif f['type'] == 'Checkbox':
                        self.assertIn(val, ['true', 'false'])
                    elif f['type'] in ('Number', 'Currency'):
                        self.assertGreaterEqual(float(val), 0)
                    elif f['type'] == 'Date':
                        datetime.strptime(val, '%Y-%m-%d')
                    if 'length' in f:
                        self.assertLessEqual(len(val), f['length'])

    def test_game_grain_formulas_null_and_zero(self):
        data = rows('Game/Data/performance.csv')
        keys = [(r['Report_Date__c'], r['Campaign_Code'], r['Channel__c']) for r in data]
        self.assertEqual(len(data), 120)
        self.assertEqual(len(set(keys)), 120)
        self.assertEqual(rows('Game/Data/performance-first10.csv'), data[:10])
        by_key = dict(zip(keys, data))
        for channel, achievement, conversion in [('Community', .62, .8), ('Video', 1.15, .5)]:
            r = by_key[('2026-10-05', 'KA3-NEW', channel)]
            self.assertAlmostEqual(int(r['Actual_Installs__c']) / int(r['Target_Installs__c']), achievement)
            self.assertAlmostEqual(int(r['First_Match_Users__c']) / int(r['Actual_Installs__c']), conversion)
        self.assertEqual(by_key[('2026-10-05','KA3-NEW','SNS')]['Actual_Installs__c'], '')
        self.assertEqual(by_key[('2026-10-04','KA3-RETURN','Offline')]['Actual_Installs__c'], '0')
        self.assertNotIn(('2026-10-06', 'KA3-NEW', 'Video'), by_key)
        for r in data:
            if r['Actual_Installs__c'] != '':
                self.assertLessEqual(int(r['First_Match_Users__c']), int(r['Actual_Installs__c']))
                self.assertLessEqual(int(r['Purchase_Users__c']), int(r['First_Match_Users__c']))
        for f in schema('Game')['fields']:
            if 'formula' in f:
                self.assertEqual(f['formulaTreatBlanksAs'], 'BlankAsBlank')
                self.assertIn('NULL', f['formula'])
                self.assertNotIn('*100', f['formula'])

    def test_eyewear_relative_time_and_reserved_keys(self):
        spec = importlib.util.spec_from_file_location('prepare_eyewear', ROOT / 'scripts/prepare_eyewear.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        t0 = '2026-10-13T10:00:00+09:00'
        payload = module.prepare(t0)
        data = payload['records']
        self.assertEqual(len(data), 10)
        self.assertFalse(payload['lookupCodesResolved'])
        by_key = {r['Source_Consultation_Key__c']: r for r in data}
        self.assertEqual(len(by_key), 10)
        self.assertNotIn('GM-ESC-D', by_key)
        self.assertNotIn('GM-ESC-E', by_key)
        self.assertEqual(by_key['GM-ESC-A']['Response_Due_At__c'], '2026-10-13T05:00:00Z')
        self.assertEqual(by_key['GM-ESC-C']['Response_Due_At__c'], '2026-10-13T00:00:00Z')
        with self.assertRaises(ValueError):
            module.prepare('2026-10-13T10:00:00')
        sla = {'일반': 48, '프리미엄': 24, '플래티넘': 4}
        for r in data:
            start = datetime.fromisoformat(r['Received_At__c'].replace('Z', '+00:00'))
            due = datetime.fromisoformat(r['Response_Due_At__c'].replace('Z', '+00:00'))
            self.assertEqual(due - start, timedelta(hours=sla[r['Customer_Tier__c']]))
            self.assertIsNone(r['Current_Handler_Code'])
            self.assertIsNone(r['Escalated_At__c'])
            self.assertEqual(r['Escalation_Status__c'], '미요청')
            if r['Needs_Manager__c']:
                self.assertTrue(r['Assistance_Reason__c'])

    def test_ai_missing_information_is_not_leaked(self):
        data = rows('AI-Sales/Data/projects.csv')
        by_key = {r['Source_Project_Key__c']: r for r in data}
        self.assertEqual(set(by_key), {'AI-POC-A','AI-POC-B','AI-POC-C','AI-POC-D'})
        self.assertEqual(by_key['AI-POC-B']['Security_Review_Status__c'], '검토 중')
        self.assertIn('아직 통과하지 않았습니다', by_key['AI-POC-B']['Request_Notes__c'])
        c = by_key['AI-POC-C']
        self.assertEqual(c['POC_Success_Criteria__c'], '')
        for value in ['1,000ms', '100token/s', '3kW']:
            self.assertNotIn(value, c['Request_Notes__c'])
        d = by_key['AI-POC-D']
        self.assertEqual(d['Project_Coordinator_Code'], '')
        self.assertNotIn('브루스', d['Request_Notes__c'])
        for r in data:
            for col in ['AI_Summary__c', 'Email_Draft__c', 'Sent_At__c']:
                self.assertEqual(r[col], '')
            self.assertEqual(r['AI_Review_Status__c'], '미검토')
            self.assertEqual(r['Email_Status__c'], '미발송')

    def test_workbook_and_documentation_contract(self):
        with zipfile.ZipFile(ROOT / 'Game/Data/screen-entry.xlsx') as z:
            ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
            values = {c.attrib['r']: c.findtext('s:v', namespaces=ns) for c in sheet.findall('.//s:c', ns)}
            for address, expected in [('B13', .6), ('C13', .8), ('B14', .5), ('C14', .6)]:
                self.assertAlmostEqual(float(values[address]), expected)
        for path in ROOT.rglob('*.md'):
            self.assertNotIn('학생', path.read_text(), str(path))
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        self.assertFalse(catalog['cleanup'])
        self.assertFalse((ROOT / 'sfdx-project.json').exists())


if __name__ == '__main__':
    unittest.main()
