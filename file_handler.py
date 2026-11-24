"""Safe, project-relative storage for pipe-delimited TXT records."""

import csv
import io
import os
import tempfile
from pathlib import Path


class FileHandler:
    def __init__(self, data_folder=None):
        # By default, data is always stored beside this Python file, not in
        # whichever directory happens to be the current working directory.
        project_folder = Path(__file__).resolve().parent
        self.data_folder = Path(data_folder).resolve() if data_folder else project_folder / "data"
        self.data_folder.mkdir(parents=True, exist_ok=True)

    def _get_path(self, filename):
        filename_path = Path(filename)
        if filename_path.name != filename or filename_path.is_absolute():
            raise ValueError("Only a file name inside the data folder is allowed.")
        return self.data_folder / filename

    @staticmethod
    def _serialize_records(records):
        """Validate and serialize every row before any destination is changed."""
        output = io.StringIO(newline="")
        writer = csv.writer(output, delimiter="|", lineterminator="\n")

        for row_number, record in enumerate(records, start=1):
            if not isinstance(record, (list, tuple)):
                raise ValueError(f"Record {row_number} must be a list or tuple.")

            safe_row = []
            for field in record:
                value = "" if field is None else str(field)
                if "|" in value or "\n" in value or "\r" in value:
                    raise ValueError(
                        f"Record {row_number} contains a pipe or newline character, "
                        "which is not allowed in a field."
                    )
                safe_row.append(value)
            writer.writerow(safe_row)

        return output.getvalue()

    def load_data(self, filename):
        path = self._get_path(filename)
        if not path.exists():
            return []

        records = []
        try:
            with path.open("r", encoding="utf-8", newline="") as file:
                reader = csv.reader(file, delimiter="|", strict=True)
                for row in reader:
                    # Ignore completely blank lines, but retain empty fields in
                    # otherwise populated rows so field-count validation can catch them.
                    if row:
                        records.append(row)
        except csv.Error as error:
            raise ValueError(f"Malformed pipe-delimited data in {filename}: {error}") from error
        return records

    def save_many(self, files_to_records):
        """Stage all files, then replace originals; roll back if commit fails."""
        if not isinstance(files_to_records, dict) or not files_to_records:
            raise ValueError("At least one filename and record collection is required.")

        # Validate and serialize every file before writing any temporary file.
        serialized = {}
        for filename, records in files_to_records.items():
            path = self._get_path(filename)
            serialized[path] = self._serialize_records(records)

        staged = {}
        originals = {}
        replaced = []
        try:
            # Stage and flush every output before replacing any original.
            for path, content in serialized.items():
                originals[path] = path.read_bytes() if path.exists() else None
                with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", newline="", dir=self.data_folder,
                    prefix=f".{path.name}.", suffix=".tmp", delete=False
                ) as temp_file:
                    temp_file.write(content)
                    temp_file.flush()
                    os.fsync(temp_file.fileno())
                    staged[path] = Path(temp_file.name)

            for path, temp_path in staged.items():
                os.replace(temp_path, path)
                replaced.append(path)

        except Exception:
            # Restore any originals already replaced, or remove newly-created files.
            rollback_errors = []
            for path in reversed(replaced):
                try:
                    original = originals[path]
                    if original is None:
                        path.unlink(missing_ok=True)
                    else:
                        with tempfile.NamedTemporaryFile(
                            mode="wb", dir=self.data_folder,
                            prefix=f".{path.name}.", suffix=".restore", delete=False
                        ) as backup_file:
                            backup_file.write(original)
                            backup_file.flush()
                            os.fsync(backup_file.fileno())
                            restore_path = Path(backup_file.name)
                        os.replace(restore_path, path)
                except Exception as rollback_error:
                    rollback_errors.append(f"{path.name}: {rollback_error}")

            if rollback_errors:
                raise OSError(
                    "Save failed and one or more rollback operations also failed: "
                    + "; ".join(rollback_errors)
                )
            raise
        finally:
            for temp_path in staged.values():
                temp_path.unlink(missing_ok=True)

    def save_data(self, filename, records):
        """Compatibility wrapper for saving a single file safely."""
        self.save_many({filename: records})
