import os
import difflib
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_deals")

def get_deal_versions(base_deal_name: str) -> List[str]:
    """
    Finds all versions of a deal (e.g., Deal_Delta_Orig, Deal_Delta_Amend1).
    """
    # Simply look for files starting with the base name
    # For demo simplicity, we assume the base name is "Deal_Delta"
    files = [f for f in os.listdir(DATA_DIR) if f.startswith(base_deal_name) and f.endswith(".txt")]
    files.sort() # Should sort Orig, Amend1, Amend2 correctly if named well
    return files

def compare_versions(file1: str, file2: str) -> Dict[str, Any]:
    path1 = os.path.join(DATA_DIR, file1)
    path2 = os.path.join(DATA_DIR, file2)
    
    with open(path1, 'r') as f: text1 = f.readlines()
    with open(path2, 'r') as f: text2 = f.readlines()
    
    diff = difflib.unified_diff(text1, text2, lineterm='', n=0)
    
    changes = []
    for line in diff:
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            continue
        changes.append(line)
        
    return {
        "version_from": file1,
        "version_to": file2,
        "changes": changes
    }

