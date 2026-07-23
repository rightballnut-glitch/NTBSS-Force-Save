#!/usr/bin/env python3
"""
NTBSS Force Save Editor - Comprehensive Item Database
Research-backed inventory, cosmetics, weapons, ninjutsu, and progression tracking
NO GAMEPLAY CHEATS - Game balance preservation focus
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class ItemReleaseStatus(Enum):
    """Track item release and availability status"""
    RELEASED = "released"
    UNRELEASED = "unreleased"
    FUTURE_DLC = "future_dlc"
    DATAMINED = "datamined"
    EVENT_ONLY = "event_only"


@dataclass
class ItemData:
    """Complete item data structure"""
    id_name: str
    display_name: str
    category: str  # weapon, ninjutsu, ultimate, cosmetic, etc
    item_type: str  # attack, defense, ranged, healer, etc
    release_status: ItemReleaseStatus = ItemReleaseStatus.RELEASED
    dlc_pack: Optional[str] = None
    season: Optional[int] = None
    description: str = ""
    acquisition_method: str = "Mentor Training / Mission Rewards"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id_name,
            "name": self.display_name,
            "category": self.category,
            "type": self.item_type,
            "status": self.release_status.value,
            "dlc": self.dlc_pack,
            "season": self.season,
            "description": self.description,
            "how_to_get": self.acquisition_method
        }


class NTBSSItemCatalog:
    """Complete researched NTBSS item catalog"""
    
    # ============ JIRAIYA DLC (Season 10) ============
    JIRAIYA_SAGE_MODE = {
        # Ninjutsu - Defense Type
        "ID_NJT_D10_001": ItemData(
            "ID_NJT_D10_001", "Toad Oil Bombs", "ninjutsu", "defense",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Defense ninjutsu - Create pools of oil to control battlefield",
            "Train with Jiraiya (Sage Mode)"
        ),
        "ID_NJT_D10_002": ItemData(
            "ID_NJT_D10_002", "Ninja Art: Needle Jizo", "ninjutsu", "defense",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Defense ninjutsu - Summon protective needle formation",
            "Train with Jiraiya (Sage Mode)"
        ),
        
        # Secret Technique (Ultimate) - Defense Type
        "ID_NJT_D10_003": ItemData(
            "ID_NJT_D10_003", "Summoning: Bring Down The House Jutsu!", "ultimate", "defense",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Defense ultimate - Summon giant toads to devastate area",
            "Train with Jiraiya (Sage Mode) - Reach Rank 10"
        ),
        
        # Weapon - Defense Type
        "ID_Weapon_D10_001": ItemData(
            "ID_Weapon_D10_001", "Smoking Pipe", "weapon", "defense",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Defense weapon - Jiraiya's iconic smoking pipe",
            "Train with Jiraiya (Sage Mode)"
        ),
        
        # Cosmetics - Hair (Unisex)
        "ID_Flag_Open_CustomHair_Jiraiya_White": ItemData(
            "ID_Flag_Open_CustomHair_Jiraiya_White", "Jiraiya White Hair", "cosmetic", "hair",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Distinctive white hair from Jiraiya",
            "Train with Jiraiya (Sage Mode)"
        ),
        
        # Cosmetics - Outfit (Male)
        "ID_Flag_Acquisition_CustomJacket_DEF_Jiraiya_001": ItemData(
            "ID_Flag_Acquisition_CustomJacket_DEF_Jiraiya_001", 
            "Jiraiya Sage Mode Top", "cosmetic", "jacket",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Jiraiya's sage mode robes top - Orange and white",
            "Train with Jiraiya (Sage Mode)"
        ),
        "ID_Flag_Open_CustomJacket_DEF_Jiraiya_001": ItemData(
            "ID_Flag_Open_CustomJacket_DEF_Jiraiya_001", 
            "Jiraiya Sage Mode Top (Shop)", "cosmetic", "jacket_shop_flag",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Makes top available in shop",
            "Internal flag"
        ),
        
        "ID_Flag_Acquisition_CustomPants_DEF_Jiraiya_001": ItemData(
            "ID_Flag_Acquisition_CustomPants_DEF_Jiraiya_001", 
            "Jiraiya Sage Mode Bottom", "cosmetic", "pants",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Jiraiya's sage mode robes bottom",
            "Train with Jiraiya (Sage Mode)"
        ),
        "ID_Flag_Open_CustomPants_DEF_Jiraiya_001": ItemData(
            "ID_Flag_Open_CustomPants_DEF_Jiraiya_001", 
            "Jiraiya Sage Mode Bottom (Shop)", "cosmetic", "pants_shop_flag",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Makes bottom available in shop",
            "Internal flag"
        ),
        
        # Cosmetics - Casual Outfit (Unisex)
        "ID_Flag_Acquisition_CustomJacket_Jiraiya_CasualShirt": ItemData(
            "ID_Flag_Acquisition_CustomJacket_Jiraiya_CasualShirt", 
            "Jiraiya Ninja Way T-Shirt", "cosmetic", "jacket",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Casual t-shirt version - unisex",
            "Train with Jiraiya (Sage Mode)"
        ),
        "ID_Flag_Open_CustomJacket_Jiraiya_CasualShirt": ItemData(
            "ID_Flag_Open_CustomJacket_Jiraiya_CasualShirt", 
            "Jiraiya Ninja Way T-Shirt (Shop)", "cosmetic", "jacket_shop_flag",
            ItemReleaseStatus.RELEASED, "Jiraiya DLC - Sage Mode", 10,
            "Makes t-shirt available in shop",
            "Internal flag"
        ),
    }
    
    # ============ COSMETICS PATTERNS ============
    # These follow patterns in the save file
    COSMETIC_PATTERNS = {
        "jackets": "ID_Flag_Acquisition_CustomJacket_<TYPE>_<NUM>",
        "pants": "ID_Flag_Acquisition_CustomPants_<TYPE>_<NUM>",
        "accessories": "ID_Flag_Acquisition_CustomAccessory_<TYPE>_<NUM>",
        "hair": "ID_Flag_Open_CustomHair_<NAME>",
        "forehead": "ID_Flag_Open_CustomForehead_<NAME>",
        "face_paint": "ID_Flag_Acquisition_CustomFacePaint_<NAME>",
    }
    
    # ============ PLACEHOLDER FOR UNRELEASED CONTENT ============
    # These should NEVER be force-unlocked to prevent corruption
    UNRELEASED_PLACEHOLDERS = {
        "ID_Flag_Acquisition_CustomJacket_FUT_*": ItemData(
            "ID_Flag_Acquisition_CustomJacket_FUT_*", "[UNRELEASED] Future Cosmetic",
            "cosmetic", "jacket", ItemReleaseStatus.UNRELEASED,
            description="Unreleased content - DO NOT UNLOCK"
        ),
        "ID_NJT_FUT_*": ItemData(
            "ID_NJT_FUT_*", "[UNRELEASED] Future Ninjutsu",
            "ninjutsu", "unknown", ItemReleaseStatus.UNRELEASED,
            description="Unreleased content - DO NOT UNLOCK"
        ),
        "ID_Weapon_FUT_*": ItemData(
            "ID_Weapon_FUT_*", "[UNRELEASED] Future Weapon",
            "weapon", "unknown", ItemReleaseStatus.UNRELEASED,
            description="Unreleased content - DO NOT UNLOCK"
        ),
    }
    
    # ============ WHAT IS NOT INCLUDED (Game Balance Preservation) ============
    # These gameplay modifiers are intentionally NOT implemented
    PROHIBITED_CHEATS = {
        "infinite_ninjutsu": "Infinite ninjutsu in matches - ruins competitive balance",
        "infinite_secret_technique": "Infinite ultimate in matches - breaks game design",
        "instant_cooldown_reset": "Instant ability cooldowns - removes skill timing",
        "negative_cooldowns": "Negative cooldowns - impossible state",
        "stat_overflow": "Stats beyond intended maximum - causes bugs",
        "gravity_manipulation": "Movement modifier exploits - breaks gameplay",
    }
    
    @staticmethod
    def get_all_released_items() -> Dict[str, ItemData]:
        """Get all released items (safe to unlock)"""
        return NTBSSItemCatalog.JIRAIYA_SAGE_MODE
    
    @staticmethod
    def get_unreleased_patterns() -> List[str]:
        """Get patterns for unreleased items (block these)"""
        return list(NTBSSItemCatalog.UNRELEASED_PLACEHOLDERS.keys())
    
    @staticmethod
    def is_safe_to_unlock(item_id: str) -> bool:
        """Check if item is safe to unlock"""
        # Check if it matches any unreleased pattern
        for pattern in NTBSSItemCatalog.get_unreleased_patterns():
            wildcard_pattern = pattern.replace("*", "")
            if wildcard_pattern in item_id:
                return False
        
        return True
    
    @staticmethod
    def get_item_info(item_id: str) -> Optional[ItemData]:
        """Get item information"""
        all_items = NTBSSItemCatalog.get_all_released_items()
        return all_items.get(item_id)


class SafeUnlockManager:
    """Manages safe, balanced item unlocking"""
    
    # Maximum safe values (prevent stat overflow)
    SAFE_MAXIMUMS = {
        "money": 999999999,
        "skill_points": 999999,
        "master_points": 99999,  # Per mentor, not total
        "scrolls": 999,  # Per type
        "playtime_minutes": 9999999,
        "experience": 99999999,
    }
    
    # What should NEVER be modified
    PROTECTED_VALUES = {
        "ID_Counter_Const_Zero",  # System constant
        "ID_Counter_NinjaTool_Use",  # Don't overflow this
    }
    
    PROHIBITED_UNLOCK_PATTERNS = [
        "Infinite",
        "Cheat",
        "Mod",
        "Hack",
        "Exploit",
        "Unreleased",
        "FUT_",  # Future items
        "DEBUG",
    ]
    
    @staticmethod
    def validate_unlock(item_id: str, category: str) -> Tuple[bool, str]:
        """
        Validate if an item can safely be unlocked
        Returns: (is_safe, reason)
        """
        # Check protected values
        if item_id in SafeUnlockManager.PROTECTED_VALUES:
            return False, "System constant - cannot modify"
        
        # Check for prohibited patterns
        for pattern in SafeUnlockManager.PROHIBITED_UNLOCK_PATTERNS:
            if pattern in item_id:
                return False, f"Prohibited pattern: {pattern}"
        
        # Check if unreleased
        if not NTBSSItemCatalog.is_safe_to_unlock(item_id):
            return False, "Item is unreleased or future content"
        
        return True, "Safe to unlock"
    
    @staticmethod
    def get_prohibited_cheats() -> Dict[str, str]:
        """Get list of prohibited cheats with explanations"""
        return NTBSSItemCatalog.PROHIBITED_CHEATS


class ItemDatabaseExporter:
    """Export item database in various formats"""
    
    @staticmethod
    def to_json() -> str:
        """Export as JSON"""
        data = {
            "jiraiya_sage_mode": {
                id: item.to_dict() 
                for id, item in NTBSSItemCatalog.JIRAIYA_SAGE_MODE.items()
            },
            "unreleased_patterns": [
                {"pattern": pattern, "reason": NTBSSItemCatalog.UNRELEASED_PLACEHOLDERS[pattern].description}
                for pattern in NTBSSItemCatalog.get_unreleased_patterns()
            ],
            "prohibited_cheats": NTBSSItemCatalog.PROHIBITED_CHEATS,
            "safe_maximums": SafeUnlockManager.SAFE_MAXIMUMS,
        }
        return json.dumps(data, indent=2, default=str)
    
    @staticmethod
    def to_markdown() -> str:
        """Export as Markdown documentation"""
        md = """# NTBSS Force Save Editor - Item Database

## Overview
This database contains all researched items, cosmetics, weapons, and ninjutsu for NTBSS.
**IMPORTANT**: This tool focuses on cosmetics and progression unlocking, NOT gameplay cheating.

## Jiraiya DLC (Season 10) - Sage Mode

### Ninjutsu & Ultimate
"""
        for item_id, item in NTBSSItemCatalog.JIRAIYA_SAGE_MODE.items():
            if item.category in ["ninjutsu", "ultimate"]:
                md += f"- **{item.display_name}** (`{item_id}`): {item.description}\n"
                md += f"  - How to get: {item.acquisition_method}\n\n"
        
        md += """
### Weapons
"""
        for item_id, item in NTBSSItemCatalog.JIRAIYA_SAGE_MODE.items():
            if item.category == "weapon":
                md += f"- **{item.display_name}** (`{item_id}`): {item.description}\n"
                md += f"  - How to get: {item.acquisition_method}\n\n"
        
        md += """
### Cosmetics
"""
        for item_id, item in NTBSSItemCatalog.JIRAIYA_SAGE_MODE.items():
            if item.category == "cosmetic":
                md += f"- **{item.display_name}** (`{item_id}`): {item.description}\n"
                md += f"  - How to get: {item.acquisition_method}\n\n"
        
        md += """
## Game Balance Preservation

This tool **DOES NOT** include gameplay cheating features:

| Prohibited | Reason |
|-----------|--------|
"""
        for cheat, reason in NTBSSItemCatalog.PROHIBITED_CHEATS.items():
            md += f"| {cheat} | {reason} |\n"
        
        md += """
## Safe Unlock Limits

To prevent save corruption and maintain game balance:

| Stat | Maximum |
|------|---------|
"""
        for stat, max_val in SafeUnlockManager.SAFE_MAXIMUMS.items():
            md += f"| {stat} | {max_val:,} |\n"
        
        return md


# Example usage
if __name__ == "__main__":
    # Export as JSON
    json_output = ItemDatabaseExporter.to_json()
    json_path = Path(__file__).parent / "item_database.json"
    json_path.write_text(json_output)
    logger.info(f"Exported item database to {json_path}")
    
    # Export as Markdown
    md_output = ItemDatabaseExporter.to_markdown()
    md_path = Path(__file__).parent / "ITEM_DATABASE.md"
    md_path.write_text(md_output)
    logger.info(f"Exported documentation to {md_path}")
    
    # Validate some items
    test_items = [
        "ID_NJT_D10_001",
        "ID_Weapon_D10_001",
        "ID_Flag_Acquisition_CustomJacket_DEF_Jiraiya_001",
    ]
    
    logger.info("\nValidation Results:")
    for item_id in test_items:
        safe, reason = SafeUnlockManager.validate_unlock(item_id, "cosmetic")
        status = "✓ SAFE" if safe else "✗ BLOCKED"
        logger.info(f"{status}: {item_id} - {reason}")
