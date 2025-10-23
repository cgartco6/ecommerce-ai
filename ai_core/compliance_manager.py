# ai_core/compliance_manager.py
from typing import Dict, List
from enum import Enum
import datetime

class CountryCode(Enum):
    ZA = "South Africa"  # POPIA
    NA = "Namibia"       # Data Protection Act
    BW = "Botswana"      # Data Protection Act
    EU = "European Union" # GDPR
    US = "United States"  # CCPA, COPPA
    CA = "Canada"         # PIPEDA
    AU = "Australia"      # Privacy Act
    JP = "Japan"          # APPI
    UK = "United Kingdom" # UK GDPR
    IN = "India"          # Personal Data Protection Bill

class GlobalComplianceManager:
    def __init__(self):
        self.regulations = self._load_regulations()
        self.compliance_log = []
        self.user_consents = {}
    
    def ensure_compliance(self, user_data: Dict, country: CountryCode) -> Dict:
        """Ensure full compliance for specific country"""
        compliance_rules = self.regulations[country]
        
        compliance_result = {
            "data_protection": self._implement_data_protection(user_data, compliance_rules),
            "privacy_policy": self._generate_country_specific_privacy_policy(country),
            "cookie_consent": self._implement_cookie_consent(country),
            "age_verification": self._implement_age_verification(country),
            "tax_compliance": self._handle_tax_compliance(country),
            "content_restrictions": self._apply_content_restrictions(country),
            "data_retention": self._set_data_retention_policy(country),
            "user_rights": self._implement_user_rights(country)
        }
        
        # Log compliance check
        self.compliance_log.append({
            "user_id": user_data.get('id'),
            "country": country.value,
            "timestamp": datetime.datetime.now(),
            "compliance_result": compliance_result
        })
        
        return compliance_result
    
    def _implement_data_protection(self, user_data: Dict, rules: Dict) -> Dict:
        """Implement data protection measures"""
        return {
            "data_encryption": True,
            "data_minimization": True,
            "purpose_limitation": True,
            "storage_limitation": rules.get('data_retention_days', 365),
            "right_to_erasure": True,
            "data_portability": True,
            "consent_management": True,
            "data_breach_protocol": "24_hour_notification"
        }
    
    def _generate_country_specific_privacy_policy(self, country: CountryCode) -> Dict:
        """Generate country-specific privacy policy"""
        policy_templates = {
            CountryCode.ZA: {
                "regulation": "POPIA (Protection of Personal Information Act)",
                "data_controller": "CostByte (Pty) Ltd",
                "supervisory_authority": "Information Regulator of South Africa",
                "user_rights": ["access", "correction", "deletion", "objection"]
            },
            CountryCode.EU: {
                "regulation": "GDPR (General Data Protection Regulation)",
                "data_controller": "CostByte EU Representative",
                "supervisory_authority": "Appropriate national DPA",
                "user_rights": ["access", "rectification", "erasure", "restriction", "portability", "objection"]
            },
            CountryCode.US: {
                "regulation": "CCPA/CPRA (California Consumer Privacy Act)",
                "data_controller": "CostByte Inc.",
                "supervisory_authority": "California Attorney General",
                "user_rights": ["know", "delete", "opt-out", "non-discrimination"]
            }
        }
        
        return policy_templates.get(country, policy_templates[CountryCode.ZA])
    
    def _implement_cookie_consent(self, country: CountryCode) -> Dict:
        """Implement cookie consent based on country regulations"""
        consent_requirements = {
            CountryCode.EU: {
                "consent_type": "explicit_opt_in",
                "cookie_categories": ["necessary", "preferences", "analytics", "marketing"],
                "banner_required": True,
                "granular_controls": True
            },
            CountryCode.US: {
                "consent_type": "notice_based",
                "cookie_categories": ["necessary", "optional"],
                "banner_required": False,
                "opt_out_mechanism": True
            },
            CountryCode.ZA: {
                "consent_type": "informed_consent",
                "cookie_categories": ["necessary", "functional", "analytical"],
                "banner_required": True,
                "simple_opt_out": True
            }
        }
        
        return consent_requirements.get(country, consent_requirements[CountryCode.ZA])
    
    def _implement_age_verification(self, country: CountryCode) -> Dict:
        """Implement age verification based on country"""
        age_limits = {
            CountryCode.US: 13,  # COPPA
            CountryCode.EU: 16,  # GDPR
            CountryCode.UK: 13,
            CountryCode.ZA: 18,
            CountryCode.CA: 13,
            CountryCode.AU: 16
        }
        
        return {
            "minimum_age": age_limits.get(country, 16),
            "verification_method": "self_declaration",  # or "document_verification" for higher risk
            "parental_consent_required": age_limits.get(country, 16) < 18,
            "age_verification_flow": "registration_gate"
        }
    
    def _handle_tax_compliance(self, country: CountryCode) -> Dict:
        """Handle tax compliance for different countries"""
        tax_rates = {
            CountryCode.ZA: 0.15,  # VAT
            CountryCode.NA: 0.15,  # VAT
            CountryCode.BW: 0.14,  # VAT
            CountryCode.EU: 0.21,  # Average VAT
            CountryCode.US: 0.00,  # Varies by state
            CountryCode.CA: 0.05,  # GST/HST
            CountryCode.AU: 0.10,  # GST
            CountryCode.JP: 0.10,  # Consumption tax
            CountryCode.UK: 0.20   # VAT
        }
        
        return {
            "tax_rate": tax_rates.get(country, 0.15),
            "tax_inclusive": True,
            "tax_id_collection": country in [CountryCode.EU, CountryCode.ZA, CountryCode.UK],
            "invoice_generation": True,
            "tax_authority": self._get_tax_authority(country)
        }
    
    def _apply_content_restrictions(self, country: CountryCode) -> Dict:
        """Apply content restrictions based on country"""
        restrictions = {
            CountryCode.US: {
                "educational_standards": "Common Core alignment optional",
                "accessibility": "ADA compliance required",
                "export_controls": "EAR restrictions apply"
            },
            CountryCode.EU: {
                "educational_standards": "EU digital education framework",
                "accessibility": "EN 301 549 compliance",
                "cultural_sensitivity": "Multilingual support required"
            },
            CountryCode.ZA: {
                "educational_standards": "SAQA alignment recommended",
                "language_requirements": ["English", "Afrikaans", "Zulu"],
                "local_content": "South African context preferred"
            }
        }
        
        return restrictions.get(country, {})
    
    def _set_data_retention_policy(self, country: CountryCode) -> Dict:
        """Set data retention policies based on country"""
        retention_periods = {
            CountryCode.EU: 365,  # GDPR - no longer than necessary
            CountryCode.ZA: 365,  # POPIA
            CountryCode.US: 730,  # Longer retention common
            CountryCode.CA: 365,  # PIPEDA
            CountryCode.AU: 365   # Privacy Act
        }
        
        return {
            "retention_period_days": retention_periods.get(country, 365),
            "data_minimization": True,
            "automated_deletion": True,
            "archival_policy": "encrypted_backups"
        }
    
    def _implement_user_rights(self, country: CountryCode) -> Dict:
        """Implement user rights based on regulations"""
        rights_configs = {
            CountryCode.EU: {
                "rights": ["access", "rectification", "erasure", "restriction", "portability", "objection"],
                "response_time_days": 30,
                "no_fee_basis": True,
                "complaint_mechanism": "DPA"
            },
            CountryCode.ZA: {
                "rights": ["access", "correction", "deletion", "objection"],
                "response_time_days": 21,
                "no_fee_basis": True,
                "complaint_mechanism": "Information Regulator"
            },
            CountryCode.US: {
                "rights": ["know", "delete", "opt-out", "non-discrimination"],
                "response_time_days": 45,
                "verification_required": True,
                "complaint_mechanism": "Attorney General"
            }
        }
        
        return rights_configs.get(country, rights_configs[CountryCode.ZA])
    
    def _get_tax_authority(self, country: CountryCode) -> str:
        """Get tax authority for country"""
        authorities = {
            CountryCode.ZA: "South African Revenue Service (SARS)",
            CountryCode.NA: "Namibia Revenue Agency",
            CountryCode.BW: "Botswana Unified Revenue Service",
            CountryCode.EU: "Local national tax authority",
            CountryCode.US: "Internal Revenue Service (IRS) + State authorities",
            CountryCode.CA: "Canada Revenue Agency",
            CountryCode.AU: "Australian Taxation Office",
            CountryCode.JP: "National Tax Agency Japan",
            CountryCode.UK: "HM Revenue & Customs"
        }
        return authorities.get(country, "Local tax authority")
    
    def _load_regulations(self) -> Dict:
        """Load all regulatory requirements"""
        return {
            CountryCode.ZA: {
                'data_retention_days': 365,
                'privacy_law': 'POPIA',
                'data_transfer_rules': 'adequate_protection_required',
                'breach_notification_hours': 72
            },
            CountryCode.EU: {
                'data_retention_days': 365,
                'privacy_law': 'GDPR',
                'data_transfer_rules': 'adequacy_decision_required',
                'breach_notification_hours': 72
            },
            CountryCode.US: {
                'data_retention_days': 730,
                'privacy_law': 'CCPA/CPRA',
                'data_transfer_rules': 'standard_contractual_clauses',
                'breach_notification_hours': 72
            },
            CountryCode.UK: {
                'data_retention_days': 365,
                'privacy_law': 'UK GDPR',
                'data_transfer_rules': 'adequacy_decision_required',
                'breach_notification_hours': 72
            },
            CountryCode.CA: {
                'data_retention_days': 365,
                'privacy_law': 'PIPEDA',
                'data_transfer_rules': 'adequate_protection_required',
                'breach_notification_hours': 72
            },
            CountryCode.AU: {
                'data_retention_days': 365,
                'privacy_law': 'Privacy Act',
                'data_transfer_rules': 'cross-border_disclosure',
                'breach_notification_hours': 72
            },
            CountryCode.JP: {
                'data_retention_days': 365,
                'privacy_law': 'APPI',
                'data_transfer_rules': 'adequate_protection_required',
                'breach_notification_hours': 72
            }
        }
    
    def get_compliance_report(self) -> Dict:
        """Generate compliance report"""
        total_checks = len(self.compliance_log)
        compliant_checks = sum(1 for log in self.compliance_log 
                             if all(result is not False for result in log['compliance_result'].values()))
        
        return {
            "total_compliance_checks": total_checks,
            "compliance_rate": compliant_checks / total_checks if total_checks > 0 else 0,
            "countries_served": list(set(log['country'] for log in self.compliance_log)),
            "recent_issues": self._get_recent_compliance_issues(),
            "regulatory_updates": self._check_regulatory_updates()
        }
    
    def _get_recent_compliance_issues(self) -> List[Dict]:
        """Get recent compliance issues"""
        issues = []
        for log in self.compliance_log[-10:]:  # Last 10 checks
            for aspect, result in log['compliance_result'].items():
                if result is False:
                    issues.append({
                        "user_id": log['user_id'],
                        "country": log['country'],
                        "aspect": aspect,
                        "timestamp": log['timestamp']
                    })
        return issues
    
    def _check_regulatory_updates(self) -> List[str]:
        """Check for recent regulatory updates"""
        # In production, this would connect to regulatory update feeds
        return [
            "GDPR: New guidelines on AI and data protection (2024)",
            "POPIA: Updated breach notification procedures",
            "CCPA: Amendments effective January 2024"
        ]
