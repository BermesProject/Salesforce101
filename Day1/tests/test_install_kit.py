import csv
from collections import Counter
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NS = {"m": "http://soap.sforce.com/2006/04/metadata"}


def read_csv(name):
    with (ROOT / "Data" / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def required_element(root, path):
    node = root.find(path, NS)
    if node is None:
        raise AssertionError(f"Missing XML element: {path}")
    return node


class ClaudeInstallKitContractTest(unittest.TestCase):
    def test_is_an_instruction_kit_not_a_salesforce_project(self):
        self.assertTrue((ROOT / "CLAUDE.md").is_file())
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertFalse((ROOT / "sfdx-project.json").exists())
        self.assertFalse((ROOT / "force-app").exists())
        self.assertFalse((ROOT / "manifest").exists())
        self.assertFalse((ROOT / "package.xml").exists())

    def test_catalog_declares_only_the_requested_metadata_categories(self):
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["format"], "claude-readable-salesforce-install-kit")
        self.assertEqual(catalog["apiVersion"], "67.0")
        self.assertEqual(
            [item["category"] for item in catalog["installOrder"]],
            ["Cleanup", "Object", "Field", "Custom App", "List View", "Access", "Flow", "Data"],
        )
        self.assertEqual(catalog["installOrder"][0]["mode"], "preview-first")
        self.assertEqual(catalog["counts"], {"objects": 1, "fields": 13, "apps": 1, "tabs": 1, "listViews": 5, "permissionSets": 1, "flows": 1})
        self.assertEqual(catalog["recordCounts"], {"accounts": 8, "contacts": 8, "inquiries": 30, "products": 12, "standardPricebookEntries": 12, "opportunities": 24, "opportunityProducts": 48})

    def test_component_folders_and_exact_inventory_exist(self):
        expected = {
            "Object": {"Consulting_Inquiry__c.object.xml"},
            "Custom App": {
                "Ohana_Consulting_Core.app.xml",
                "Consulting_Inquiry__c.tab.xml",
            },
            "Flow": {"Consulting_Inquiry_Escalation_Lab.flow.xml"},
            "List View": {
                "Account.AllAccounts.listView.xml",
                "Contact.AllContacts.listView.xml",
                "Opportunity.AllOpportunities.listView.xml",
                "Product2.AllProducts.listView.xml",
                "Consulting_Inquiry__c.All_Consulting_Inquiries.listView.xml",
            },
        }
        for folder, names in expected.items():
            actual = {p.name for p in (ROOT / folder).glob("*.xml")}
            self.assertEqual(actual, names)
        fields = {p.name for p in (ROOT / "Field").glob("*.field.xml")}
        self.assertEqual(
            fields,
            {
                "Assigned_Consultant__c.field.xml",
                "Attention_Reason__c.field.xml",
                "Core_Problem__c.field.xml",
                "Customer_Account__c.field.xml",
                "Customer_Contact__c.field.xml",
                "Desired_Outcome__c.field.xml",
                "Inquiry_Channel__c.field.xml",
                "Inquiry_Status__c.field.xml",
                "Inquiry_Title__c.field.xml",
                "Manager_Attention__c.field.xml",
                "Next_Contact_Date__c.field.xml",
                "Priority__c.field.xml",
                "Received_Date__c.field.xml",
            },
        )

    def test_object_is_standalone_and_has_no_flexipage_dependency(self):
        root = ET.parse(ROOT / "Object/Consulting_Inquiry__c.object.xml").getroot()
        self.assertEqual(root.findtext("m:label", namespaces=NS), "Consulting Inquiry")
        self.assertEqual(root.findtext("m:deploymentStatus", namespaces=NS), "Deployed")
        self.assertEqual(root.findtext("m:sharingModel", namespaces=NS), "ReadWrite")
        self.assertEqual(root.findall("m:actionOverrides", NS), [])

    def test_app_navigation_and_tab_dependency_are_explicit(self):
        app = ET.parse(ROOT / "Custom App/Ohana_Consulting_Core.app.xml").getroot()
        self.assertEqual(app.findtext("m:label", namespaces=NS), "Ohana Consulting")
        self.assertEqual(
            [node.text for node in app.findall("m:tabs", NS)],
            [
                "standard-Account",
                "standard-Contact",
                "Consulting_Inquiry__c",
                "standard-Opportunity",
                "standard-Task",
            ],
        )
        tab = ET.parse(ROOT / "Custom App/Consulting_Inquiry__c.tab.xml").getroot()
        self.assertEqual(tab.findtext("m:customObject", namespaces=NS), "true")

    def test_list_views_show_key_fields_and_only_adjust_standard_all_views(self):
        expected = {
            "Account.AllAccounts.listView.xml": (
                "AllAccounts",
                "All Accounts",
                ["ACCOUNT.NAME", "ACCOUNT.INDUSTRY", "ACCOUNT.URL", "CORE.USERS.ALIAS"],
            ),
            "Contact.AllContacts.listView.xml": (
                "AllContacts",
                "All Contacts",
                ["FULL_NAME", "ACCOUNT.NAME", "CONTACT.DEPARTMENT", "CONTACT.EMAIL", "CORE.USERS.ALIAS"],
            ),
            "Opportunity.AllOpportunities.listView.xml": (
                "AllOpportunities",
                "All Opportunities",
                ["OPPORTUNITY.NAME", "ACCOUNT.NAME", "OPPORTUNITY.STAGE_NAME", "OPPORTUNITY.AMOUNT", "OPPORTUNITY.CLOSE_DATE", "OPPORTUNITY.NEXT_STEP", "CORE.USERS.ALIAS"],
            ),
            "Product2.AllProducts.listView.xml": (
                "AllProducts",
                "All Products",
                ["PRODUCT2.NAME", "PRODUCT2.CUSTOMER_PRODUCT_ID", "PRODUCT2.FAMILY", "PRODUCT2.ACTIVE"],
            ),
            "Consulting_Inquiry__c.All_Consulting_Inquiries.listView.xml": (
                "All_Consulting_Inquiries",
                "All Consulting Inquiries",
                ["NAME", "Inquiry_Title__c", "Customer_Account__c", "Customer_Contact__c", "Inquiry_Status__c", "Priority__c", "Assigned_Consultant__c", "Next_Contact_Date__c", "Manager_Attention__c"],
            ),
        }
        for name, (full_name, label, columns) in expected.items():
            root = ET.parse(ROOT / "List View" / name).getroot()
            self.assertEqual(root.findtext("m:fullName", namespaces=NS), full_name)
            self.assertEqual(root.findtext("m:label", namespaces=NS), label)
            self.assertEqual(root.findtext("m:filterScope", namespaces=NS), "Everything")
            self.assertEqual([node.text for node in root.findall("m:columns", NS)], columns)
            self.assertEqual(root.findall("m:filters", NS), [], name)

    def test_flow_is_the_single_draft_inspection_flow(self):
        flow_path = ROOT / "Flow/Consulting_Inquiry_Escalation_Lab.flow.xml"
        flow = ET.parse(flow_path).getroot()
        self.assertEqual(flow.findtext("m:status", namespaces=NS), "Draft")
        self.assertEqual(flow.findtext("m:processType", namespaces=NS), "AutoLaunchedFlow")
        self.assertEqual(flow.findtext("m:start/m:object", namespaces=NS), "Consulting_Inquiry__c")
        text_files = [
            p
            for p in ROOT.rglob("*")
            if p.is_file()
            and "tests" not in p.parts
            and p.suffix in {".md", ".json", ".xml"}
        ]
        all_text = " ".join(p.read_text(encoding="utf-8") for p in text_files)
        self.assertNotIn("Consulting_Inquiry_Follow_Up_Task.flow", all_text)
        self.assertNotIn("Consulting_Inquiry_Daily_Attention_Task.flow", all_text)

    def test_fields_preserve_role_and_relationship_contracts(self):
        assigned = ET.parse(ROOT / "Field/Assigned_Consultant__c.field.xml").getroot()
        values = [
            node.text
            for node in assigned.findall(
                "m:valueSet/m:valueSetDefinition/m:value/m:fullName", NS
            )
        ]
        self.assertEqual(values, ["석유진", "조우찬", "이채원"])
        account = ET.parse(ROOT / "Field/Customer_Account__c.field.xml").getroot()
        contact = ET.parse(ROOT / "Field/Customer_Contact__c.field.xml").getroot()
        self.assertEqual(account.findtext("m:referenceTo", namespaces=NS), "Account")
        self.assertEqual(contact.findtext("m:referenceTo", namespaces=NS), "Contact")
        expected_types = {
            "Assigned_Consultant__c": "Picklist",
            "Attention_Reason__c": "Text",
            "Core_Problem__c": "LongTextArea",
            "Customer_Account__c": "Lookup",
            "Customer_Contact__c": "Lookup",
            "Desired_Outcome__c": "LongTextArea",
            "Inquiry_Channel__c": "Picklist",
            "Inquiry_Status__c": "Picklist",
            "Inquiry_Title__c": "Text",
            "Manager_Attention__c": "Checkbox",
            "Next_Contact_Date__c": "Date",
            "Priority__c": "Picklist",
            "Received_Date__c": "Date",
        }
        for path in (ROOT / "Field").glob("*.field.xml"):
            field = ET.parse(path).getroot()
            api_name = field.findtext("m:fullName", namespaces=NS) or ""
            self.assertEqual(path.name, f"{api_name}.field.xml")
            self.assertEqual(field.findtext("m:type", namespaces=NS), expected_types[api_name])
        self.assertIn(
            "TODAY()",
            ET.parse(ROOT / "Field/Attention_Reason__c.field.xml")
            .getroot()
            .findtext("m:formula", namespaces=NS)
            or "",
        )
        self.assertIn(
            "TODAY()",
            ET.parse(ROOT / "Field/Manager_Attention__c.field.xml")
            .getroot()
            .findtext("m:formula", namespaces=NS)
            or "",
        )

    def test_prohibited_deployable_categories_are_absent(self):
        prohibited_suffixes = {".cls", ".js", ".html", ".css", ".profile-meta.xml"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or "tests" in path.parts:
                continue
            self.assertFalse(
                any(path.name.endswith(suffix) for suffix in prohibited_suffixes),
                path,
            )
        for name in ["lwc", "classes", "flexipages", "profiles"]:
            self.assertFalse(any(path.name.lower() == name for path in ROOT.rglob("*")))

    def test_system_admin_access_bundle_grants_complete_custom_access(self):
        path = ROOT / "Access/Salesforce101_Day1_System_Admin_Access.permissionset.xml"
        permission_set = ET.parse(path).getroot()
        self.assertEqual(
            permission_set.findtext("m:label", namespaces=NS),
            "Salesforce 101 Day 1 System Admin Access",
        )
        app = required_element(permission_set, "m:applicationVisibilities")
        self.assertEqual(app.findtext("m:application", namespaces=NS), "Ohana_Consulting_Core")
        self.assertEqual(app.findtext("m:visible", namespaces=NS), "true")
        object_permissions = {
            node.findtext("m:object", namespaces=NS): node
            for node in permission_set.findall("m:objectPermissions", NS)
        }
        self.assertEqual(
            set(object_permissions),
            {"Account", "Contact", "Opportunity", "Product2", "Pricebook2", "Consulting_Inquiry__c"},
        )
        for object_name, object_access in object_permissions.items():
            for key in ["allowCreate", "allowDelete", "allowEdit", "allowRead", "modifyAllRecords", "viewAllFields", "viewAllRecords"]:
                self.assertEqual(object_access.findtext(f"m:{key}", namespaces=NS), "true", (object_name, key))
        permissions = {
            node.findtext("m:field", namespaces=NS): (
                node.findtext("m:readable", namespaces=NS),
                node.findtext("m:editable", namespaces=NS),
            )
            for node in permission_set.findall("m:fieldPermissions", NS)
        }
        self.assertEqual(
            set(permissions),
            {
                "Consulting_Inquiry__c.Assigned_Consultant__c",
                "Consulting_Inquiry__c.Attention_Reason__c",
                "Consulting_Inquiry__c.Core_Problem__c",
                "Consulting_Inquiry__c.Customer_Account__c",
                "Consulting_Inquiry__c.Customer_Contact__c",
                "Consulting_Inquiry__c.Desired_Outcome__c",
                "Consulting_Inquiry__c.Inquiry_Channel__c",
                "Consulting_Inquiry__c.Inquiry_Status__c",
                "Consulting_Inquiry__c.Manager_Attention__c",
                "Consulting_Inquiry__c.Next_Contact_Date__c",
                "Consulting_Inquiry__c.Priority__c",
            },
        )
        self.assertNotIn("Consulting_Inquiry__c.Inquiry_Title__c", permissions)
        self.assertNotIn("Consulting_Inquiry__c.Received_Date__c", permissions)
        for field, values in permissions.items():
            self.assertEqual(values[0], "true", field)
            expected_editable = "false" if field in {
                "Consulting_Inquiry__c.Attention_Reason__c",
                "Consulting_Inquiry__c.Manager_Attention__c",
            } else "true"
            self.assertEqual(values[1], expected_editable, field)
        tab = required_element(permission_set, "m:tabSettings")
        self.assertEqual(tab.findtext("m:tab", namespaces=NS), "Consulting_Inquiry__c")
        self.assertEqual(tab.findtext("m:visibility", namespaces=NS), "Available")

    def test_complete_practice_dataset_is_portable_and_relational(self):
        accounts = read_csv("accounts.csv")
        contacts = read_csv("contacts.csv")
        inquiries = read_csv("inquiries.csv")
        products = read_csv("products.csv")
        opportunities = read_csv("opportunities.csv")
        lines = read_csv("opportunity-products.csv")
        self.assertEqual(list(accounts[0]), ["Name", "Industry", "Website", "Description"])
        self.assertEqual(list(contacts[0]), ["AccountName", "FirstName", "LastName", "Email", "Department"])
        self.assertEqual(
            list(inquiries[0]),
            ["ReferenceKey", "AccountName", "ContactEmail", "Inquiry_Title__c", "Inquiry_Channel__c", "Inquiry_Status__c", "Core_Problem__c", "Desired_Outcome__c", "Priority__c", "Received_Date__c", "Next_Contact_Date__c", "Assigned_Consultant__c"],
        )
        self.assertEqual(list(products[0]), ["ProductCode", "Name", "Family", "Description", "IsActive", "StandardPrice", "PricebookEntryIsActive", "UseStandardPrice"])
        self.assertEqual(list(opportunities[0]), ["OpportunityName", "AccountName", "StageName", "CloseDate", "Description", "NextStep", "Amount"])
        self.assertEqual(list(lines[0]), ["OpportunityName", "ProductCode", "Quantity", "UnitPrice", "TotalPrice", "Description"])
        self.assertEqual(
            (len(accounts), len(contacts), len(inquiries), len(products), len(opportunities), len(lines)),
            (8, 8, 30, 12, 24, 48),
        )
        account_names = {row["Name"] for row in accounts}
        contact_emails = {row["Email"] for row in contacts}
        product_codes = {row["ProductCode"] for row in products}
        opportunity_names = {row["OpportunityName"] for row in opportunities}
        self.assertEqual(len(account_names), 8)
        self.assertEqual(len(contact_emails), 8)
        self.assertEqual(len(product_codes), 12)
        self.assertEqual(len(opportunity_names), 24)
        self.assertTrue(all(row["AccountName"] in account_names for row in contacts))
        account_by_email = {row["Email"]: row["AccountName"] for row in contacts}
        self.assertEqual(len(account_by_email), 8)
        self.assertTrue(all(row["AccountName"] in account_names for row in inquiries))
        self.assertEqual(sum(not row["ContactEmail"] for row in inquiries), 1)
        self.assertTrue(all(not row["ContactEmail"] or row["ContactEmail"] in contact_emails for row in inquiries))
        self.assertTrue(all(not row["ContactEmail"] or account_by_email[row["ContactEmail"]] == row["AccountName"] for row in inquiries))
        self.assertEqual(Counter(row["Assigned_Consultant__c"] for row in inquiries), Counter({"석유진": 10, "조우찬": 10, "이채원": 10}))
        self.assertTrue(all(row["AccountName"] in account_names for row in opportunities))
        self.assertEqual(Counter(row["AccountName"] for row in opportunities), Counter({name: 3 for name in account_names}))
        self.assertTrue(all(row["OpportunityName"] in opportunity_names for row in lines))
        self.assertTrue(all(row["ProductCode"] in product_codes for row in lines))
        self.assertEqual(Counter(row["OpportunityName"] for row in lines), Counter({name: 2 for name in opportunity_names}))
        self.assertEqual(len({(row["OpportunityName"], row["ProductCode"]) for row in lines}), 48)
        price_by_code = {row["ProductCode"]: int(row["StandardPrice"]) for row in products}
        amount_by_opportunity = {row["OpportunityName"]: int(row["Amount"]) for row in opportunities}
        sums = Counter()
        for row in lines:
            self.assertEqual(row["Quantity"], "1")
            self.assertEqual(int(row["UnitPrice"]), price_by_code[row["ProductCode"]])
            self.assertEqual(int(row["TotalPrice"]), int(row["Quantity"]) * int(row["UnitPrice"]))
            sums[row["OpportunityName"]] += int(row["TotalPrice"])
        self.assertEqual(dict(sums), amount_by_opportunity)
        serialized = " ".join(path.read_text(encoding="utf-8") for path in (ROOT / "Data").glob("*.csv"))
        self.assertNotRegex(serialized, r"\b(?:001|003|006|00Q|00k)[A-Za-z0-9]{12}(?:[A-Za-z0-9]{3})?\b")
        self.assertNotIn("OwnerId", serialized)

    def test_data_and_access_runbooks_are_fail_closed(self):
        data = (ROOT / "Data/README.md").read_text(encoding="utf-8")
        access = (ROOT / "Access/README.md").read_text(encoding="utf-8")
        list_views = (ROOT / "List View/README.md").read_text(encoding="utf-8")
        for phrase in ["EMPTY", "COMPLETE", "PARTIAL", "Savepoint", "rollback", "Owner", "설치·실행한 교육생", "DML 0", "read-back"]:
            self.assertIn(phrase, data)
        for phrase in ["System Administrator", "PermissionSetAssignment", "명시적 승인", "objectPermissions", "fieldPermissions", "applicationVisibilities", "View All Fields", "Available"]:
            self.assertIn(phrase, access)
        for phrase in ["AllAccounts", "AllContacts", "AllOpportunities", "AllProducts", "All_Consulting_Inquiries", "표시 열만", "filterScope", "label", "filters"]:
            self.assertIn(phrase, list_views)

    def test_cleanup_policy_is_preview_first_and_fail_closed(self):
        policy = (ROOT / "Cleanup/README.md").read_text(encoding="utf-8")
        required = [
            "정확한 Account ID",
            "명시적 승인",
            "RUN_DELETE = false",
            "Savepoint",
            "rollback",
            "OpportunityLineItem → Task/Event → Case → Opportunity → Contact → Account",
            "soft delete",
            "Product2",
            "PricebookEntry",
            "Lead",
            "Campaign",
            "교육생이 만든 레코드",
            "Customer_Account__c",
            "Customer_Contact__c",
            "SetNull",
            "참조 중이면 중단",
            "승인 화면에만 일시적으로 표시",
            "저장소 밖",
            "즉시 삭제",
        ]
        for phrase in required:
            self.assertIn(phrase, policy)
        self.assertNotIn("DELETE FROM", policy.upper())

    def test_claude_contract_places_cleanup_before_metadata(self):
        contract = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertLess(contract.index("샘플 데이터 정리"), contract.index("임시 payload 구성"))
        for phrase in [
            "Cleanup/README.md",
            "삭제 후보 preview",
            "정확한 Account ID",
            "명시적 승인",
            "Product2",
            "PricebookEntry",
            "hard delete",
            "승인 화면에만 일시적으로 표시",
            "`Consulting_Inquiry__c` 참조",
        ]:
            self.assertIn(phrase, contract)

    def test_claude_contract_requires_preview_approval_and_readback(self):
        contract = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for phrase in [
            "Developer Edition",
            "dry-run",
            "명시적 승인",
            "Cleanup → Object → Field → Custom App → List View → Access → Flow → Data",
            "Draft",
            "활성화하지",
            "read-back",
            "OwnerId",
            "ActiveVersionId",
            "LatestVersionId",
            "같은 Developer Edition",
            "활성 버전이 있으면 중단",
        ]:
            self.assertIn(phrase, contract)
        self.assertNotRegex(contract, r"--target-org\s+[A-Za-z0-9_-]+")
        self.assertNotRegex(contract, r"\b00D[A-Za-z0-9]{12}(?:[A-Za-z0-9]{3})?\b")


if __name__ == "__main__":
    unittest.main()
