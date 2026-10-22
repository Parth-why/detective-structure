"""
Asset Manager Service for Social Detective.
Discovers and manages visual assets in static/assets/ and its subdirectories.
Preserves existing assets and automatically maps backgrounds, character portraits,
evidence photos, cursors, textures, and icons.
"""
import os
import glob

class AssetManagerService:
    def __init__(self, static_dir=None):
        if static_dir is None:
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
        self.static_dir = static_dir
        self.assets_dir = os.path.join(self.static_dir, "assets")
        self._ensure_asset_directories()

    def _ensure_asset_directories(self):
        """Ensure standard asset subdirectories exist without removing any user files."""
        try:
            subdirs = ["backgrounds", "characters", "evidence", "icons", "textures", "cursors"]
            if not os.path.exists(self.assets_dir):
                os.makedirs(self.assets_dir, exist_ok=True)
            for s in subdirs:
                target = os.path.join(self.assets_dir, s)
                if not os.path.exists(target):
                    os.makedirs(target, exist_ok=True)
        except OSError:
            pass

    def scan_assets(self):
        """
        Recursively scan static/assets/ to catalog all available visual assets.
        Supports files placed directly in static/assets/ or organized in subdirectories.
        """
        valid_exts = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}
        all_files = []

        if os.path.exists(self.assets_dir):
            for root, _, files in os.walk(self.assets_dir):
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in valid_exts:
                        full_path = os.path.join(root, f)
                        rel_path = os.path.relpath(full_path, self.static_dir).replace("\\", "/")
                        all_files.append({
                            "filename": f,
                            "rel_url": f"/static/{rel_path}",
                            "path": full_path,
                            "ext": ext
                        })

        # Categorize assets dynamically
        board_bg = self._find_board_background(all_files)
        cursor_asset = self._find_cursor_asset(all_files)
        characters = self._map_characters(all_files)
        evidence_images = self._map_evidence(all_files)

        return {
            "board_background": board_bg,
            "cursor_asset": cursor_asset,
            "characters": characters,
            "evidence": evidence_images,
            "all_assets": [a["rel_url"] for a in all_files],
            "total_assets": len(all_files)
        }

    def _find_board_background(self, assets):
        """Find the investigation board background image."""
        bg_keywords = ["board", "desk", "background", "bg", "investigation", "table", "noir", "case_board", "wood"]
        
        # 1. Search in backgrounds/ subdirectory first
        for a in assets:
            if "backgrounds" in a["rel_url"].lower():
                return a["rel_url"]

        # 2. Search by keywords across static/assets/
        for a in assets:
            name_lower = a["filename"].lower()
            if any(k in name_lower for k in bg_keywords) and not ("glass" in name_lower or "cursor" in name_lower or "monocle" in name_lower):
                return a["rel_url"]

        # 3. If any image exists in static/assets/ that is not a cursor/monocle
        for a in assets:
            name_lower = a["filename"].lower()
            if not ("glass" in name_lower or "monocle" in name_lower or "cursor" in name_lower):
                return a["rel_url"]

        # 4. Fallback if no background image is uploaded
        return None

    def _find_cursor_asset(self, assets):
        """Find custom magnifying glass or monocle cursor image."""
        cursor_keywords = ["glass", "monocle", "magnif", "lens", "cursor", "retro_gentleman"]
        for a in assets:
            name_lower = a["filename"].lower()
            if any(k in name_lower for k in cursor_keywords):
                return a["rel_url"]

        # Default to the existing monocle asset if present in root
        default_monocle = "/static/assets/Glass_Pieces_PNG_Transparent__Glasses_Single_Piece_Retro_Gentleman__Monocle__Glasses__Vintage_PNG_Image_For_Free_Download-removebg-preview.png"
        return default_monocle

    def _map_characters(self, assets):
        """Map suspect portraits by id or name."""
        char_map = {}
        cursor_and_bg_keywords = ["glass", "monocle", "cursor", "background", "board", "desk", "wood"]
        for a in assets:
            rel_lower = a["rel_url"].lower()
            name_no_ext = os.path.splitext(a["filename"])[0].lower()
            if "characters" in rel_lower or ("character" in name_no_ext or "suspect" in name_no_ext or "portrait" in name_no_ext):
                char_map[name_no_ext] = a["rel_url"]
            elif not any(k in name_no_ext for k in cursor_and_bg_keywords) and "backgrounds" not in rel_lower and "cursors" not in rel_lower:
                char_map[name_no_ext] = a["rel_url"]
        return char_map

    def _map_evidence(self, assets):
        """Map evidence photos by numeric ID or title."""
        ev_map = {}
        cursor_and_bg_keywords = ["glass", "monocle", "cursor", "background", "board", "desk", "wood"]
        for a in assets:
            rel_lower = a["rel_url"].lower()
            name_no_ext = os.path.splitext(a["filename"])[0].lower()
            if "evidence" in rel_lower or ("evidence" in name_no_ext or "clue" in name_no_ext or "photo" in name_no_ext or "log" in name_no_ext):
                ev_map[name_no_ext] = a["rel_url"]
            elif not any(k in name_no_ext for k in cursor_and_bg_keywords) and "backgrounds" not in rel_lower and "cursors" not in rel_lower:
                ev_map[name_no_ext] = a["rel_url"]
        return ev_map
