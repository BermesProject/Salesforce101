import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NS = {"m": "http://soap.sforce.com/2006/04/metadata"}


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
            ["Object", "Field", "Custom App", "Flow"],
        )
        self.assertEqual(catalog["counts"], {"objects": 1, "fields": 13, "apps": 1, "tabs": 1, "flows": 1})

    def test_component_folders_and_exact_inventory_exist(self):
        expected = {
            "Object": {"Consulting_Inquiry__c.object.xml"},
            "Custom App": {
                "Ohana_Consulting_Core.app.xml",
                "Consulting_Inquiry__c.tab.xml",
            },
            "Flow": {"Consulting_Inquiry_Escalation_Lab.flow.xml"},
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
        prohibited_suffixes = {".cls", ".js", ".html", ".css", ".permissionset-meta.xml"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or "tests" in path.parts:
                continue
            self.assertFalse(
                any(path.name.endswith(suffix) for suffix in prohibited_suffixes),
                path,
            )
        for name in ["lwc", "classes", "flexipages", "permissionsets", "profiles"]:
            self.assertFalse(any(path.name.lower() == name for path in ROOT.rglob("*")))

    def test_claude_contract_requires_preview_approval_and_readback(self):
        contract = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for phrase in [
            "Developer Edition",
            "dry-run",
            "명시적 승인",
            "Object → Field → Custom App → Flow",
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
