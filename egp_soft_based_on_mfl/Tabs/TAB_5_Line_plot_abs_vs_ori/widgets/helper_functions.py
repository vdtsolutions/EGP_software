import pandas as pd
import os
import tempfile
import shutil
from pathlib import Path


def safe_read_pickle(self, path):
    print("starting safe pkl function read")
    import pickle
    if not os.path.exists(path):
        return None
    if os.path.getsize(path) == 0:
        print("[WARN] Pickle is empty.")
        try:
            os.remove(path)
        except:
            pass
        return None
    try:
        return pd.read_pickle(path)
    except (pickle.UnpicklingError, EOFError, ValueError) as e:
        print(f"[WARN] Pickle unreadable ({e}). Rebuilding...")
        try:
            os.remove(path)
        except:
            pass
            return None






def save_pickle_safely(self, path, df_new):
    """
    Safe, atomic-ish pickle write in the same directory:
      1) write to a temp file in path.parent
      2) move/replace to final path
    Logs the same messages as your inline block.
    Returns True on success, False on failure.
    """
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        tmpfile = tempfile.NamedTemporaryFile(delete=False, dir=path.parent, suffix=".tmp")
        tmpname = tmpfile.name
        try:
            # Write pickle to temp file
            df_new.to_pickle(tmpname)
        finally:
            tmpfile.close()

        # Move temp -> final (same dir, so it should be atomic on most filesystems)
        shutil.move(tmpname, str(path))
        self.config.print_with_time(f"Saved pickle safely: {path}")
        return True

    except Exception as e:
        self.config.print_with_time(f"❌ Failed to save pickle: {e}")
        # Best effort cleanup if temp still exists
        try:
            if 'tmpname' in locals() and os.path.exists(tmpname):
                os.remove(tmpname)
        except Exception:
            pass
        return False




def fetch_weld_range(self, cursor, runid, weld_num):

    query = """
        SELECT start_index, end_index, start_oddo1, end_oddo1 
        FROM welds 
        WHERE runid=%s 
          AND id IN (%s, (SELECT MAX(id) FROM welds WHERE runid=%s AND id < %s))
        ORDER BY id
    """

    cursor.execute(query, (runid, weld_num, runid, weld_num))
    result = cursor.fetchall()

    if not result:
        self.config.print_with_time("NO WELD SELECTED OR FETCHED IN SHOW DATA -- FIRST TRY FETCHING THEN RETRY ")
        return None

    return result
