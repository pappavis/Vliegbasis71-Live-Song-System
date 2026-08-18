#!/usr/bin/env python3
"""
muscriptor_batch.py

Cross-platform MP3 batch converter/transcriber for MuScriptor.

- MIDI and sheet music are produced by MuScriptor.
- WAV is produced by ffmpeg.
- CLI mode is used when command-line options are supplied.
- With no command-line options, a Tkinter desktop UI is started.
- Configuration can be saved to a .cfg file next to this script.

Python: 3.10+
Platforms: macOS, Windows, Linux
"""

from __future__ import annotations

import argparse
import configparser
import os
import shlex
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class AppSettings:
    input_dir: Path
    output_dir: Path
    muscriptor_command: str
    ffmpeg_command: str
    default_format: str


@dataclass(slots=True)
class ConversionJob:
    source: Path
    output_format: str


class ConfigurationManager:
    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path

    @property
    def config_path(self) -> Path:
        return self._config_path

    def load(self, fallback: AppSettings) -> AppSettings:
        parser = configparser.ConfigParser()
        if not self._config_path.exists():
            return fallback

        parser.read(self._config_path, encoding="utf-8")
        section = parser["settings"] if parser.has_section("settings") else {}

        return AppSettings(
            input_dir=Path(section.get("input_dir", str(fallback.input_dir))).expanduser(),
            output_dir=Path(section.get("output_dir", str(fallback.output_dir))).expanduser(),
            muscriptor_command=section.get(
                "muscriptor_command", fallback.muscriptor_command
            ),
            ffmpeg_command=section.get("ffmpeg_command", fallback.ffmpeg_command),
            default_format=section.get("default_format", fallback.default_format),
        )

    def save(self, settings: AppSettings) -> None:
        parser = configparser.ConfigParser()
        parser["settings"] = {
            "input_dir": str(settings.input_dir),
            "output_dir": str(settings.output_dir),
            "muscriptor_command": settings.muscriptor_command,
            "ffmpeg_command": settings.ffmpeg_command,
            "default_format": settings.default_format,
        }

        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        with self._config_path.open("w", encoding="utf-8") as handle:
            parser.write(handle)


class CommandBuilder:
    def __init__(
        self,
        muscriptor_command: str,
        ffmpeg_command: str,
        windows: bool | None = None,
    ) -> None:
        self._muscriptor_command = muscriptor_command
        self._ffmpeg_command = ffmpeg_command
        self._windows = os.name == "nt" if windows is None else windows

    def _split_command(self, value: str) -> list[str]:
        return shlex.split(value, posix=not self._windows)

    def build_midi(self, source: Path, output_file: Path) -> list[str]:
        return [
            *self._split_command(self._muscriptor_command),
            "transcribe",
            str(source),
            "-o",
            str(output_file),
        ]

    def build_sheets(self, source: Path, output_dir: Path) -> list[str]:
        return [
            *self._split_command(self._muscriptor_command),
            "transcribe",
            str(source),
            "--format",
            "sheets",
            "--output",
            str(output_dir),
        ]

    def build_wav(self, source: Path, output_file: Path) -> list[str]:
        return [
            *self._split_command(self._ffmpeg_command),
            "-y",
            "-i",
            str(source),
            "-vn",
            "-c:a",
            "pcm_s16le",
            str(output_file),
        ]


class Converter:
    VALID_FORMATS = ("midi", "wav", "sheet")

    def __init__(
        self,
        settings: AppSettings,
        runner: callable | None = None,
    ) -> None:
        self._settings = settings
        self._builder = CommandBuilder(
            settings.muscriptor_command,
            settings.ffmpeg_command,
        )
        self._runner = runner or subprocess.run

    def convert(
        self,
        jobs: Iterable[ConversionJob],
        on_message: callable | None = None,
    ) -> bool:
        all_ok = True
        self._settings.output_dir.mkdir(parents=True, exist_ok=True)

        for job in jobs:
            self._validate_job(job)
            self._emit(on_message, f"Start: {job.source.name} -> {job.output_format}")

            try:
                command, expected = self._command_for(job)
                self._emit(
                    on_message,
                    "Commando: " + subprocess.list2cmdline(command),
                )
                self._runner(command, check=True)

                if expected is not None and not expected.exists():
                    raise RuntimeError(
                        f"Proces eindigde zonder verwachte uitvoer: {expected}"
                    )

                self._emit(on_message, f"Klaar: {job.source.name}")
            except (subprocess.CalledProcessError, OSError, RuntimeError) as exc:
                all_ok = False
                self._emit(on_message, f"FOUT bij {job.source.name}: {exc}")

        return all_ok

    def _validate_job(self, job: ConversionJob) -> None:
        if job.output_format not in self.VALID_FORMATS:
            raise ValueError(f"Onbekend uitvoerformaat: {job.output_format}")
        if not job.source.is_file():
            raise FileNotFoundError(job.source)

    def _command_for(self, job: ConversionJob) -> tuple[list[str], Path | None]:
        stem = job.source.stem

        if job.output_format == "midi":
            output_file = self._settings.output_dir / f"{stem}.mid"
            return self._builder.build_midi(job.source, output_file), output_file

        if job.output_format == "wav":
            output_file = self._settings.output_dir / f"{stem}.wav"
            return self._builder.build_wav(job.source, output_file), output_file

        sheet_dir = self._settings.output_dir / stem
        sheet_dir.mkdir(parents=True, exist_ok=True)
        expected_midi = sheet_dir / "score.mid"
        return self._builder.build_sheets(job.source, sheet_dir), expected_midi

    @staticmethod
    def _emit(callback: callable | None, message: str) -> None:
        if callback:
            callback(message)


class JobResolver:
    def __init__(self, input_dir: Path) -> None:
        self._input_dir = input_dir

    def resolve(
        self,
        explicit_files: list[str] | None,
        default_format: str,
        overrides: dict[str, str],
    ) -> list[ConversionJob]:
        files = (
            self._resolve_explicit(explicit_files)
            if explicit_files
            else sorted(self._input_dir.glob("*.mp3"))
        )

        jobs: list[ConversionJob] = []
        for source in files:
            key_variants = (source.name, str(source), source.stem)
            selected_format = default_format
            for key in key_variants:
                if key in overrides:
                    selected_format = overrides[key]
                    break
            jobs.append(ConversionJob(source=source, output_format=selected_format))
        return jobs

    def _resolve_explicit(self, explicit_files: list[str]) -> list[Path]:
        resolved: list[Path] = []
        for value in explicit_files:
            candidate = Path(value).expanduser()
            if not candidate.is_absolute():
                candidate = self._input_dir / candidate
            resolved.append(candidate)
        return resolved


class DesktopApp:
    def __init__(
        self,
        settings: AppSettings,
        config_manager: ConfigurationManager,
    ) -> None:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk

        self._tk = tk
        self._filedialog = filedialog
        self._messagebox = messagebox
        self._ttk = ttk
        self._config_manager = config_manager
        self._root = tk.Tk()
        self._root.title("MuScriptor MP3 converter")
        self._root.geometry("980x680")
        self._root.minsize(860, 560)

        self._input_var = tk.StringVar(value=str(settings.input_dir))
        self._output_var = tk.StringVar(value=str(settings.output_dir))
        self._muscriptor_var = tk.StringVar(value=settings.muscriptor_command)
        self._ffmpeg_var = tk.StringVar(value=settings.ffmpeg_command)
        self._default_format_var = tk.StringVar(value=settings.default_format)
        self._status_var = tk.StringVar(value="Gereed")
        self._file_formats: dict[str, str] = {}

        self._build_ui()
        self._refresh_files()

    def run(self) -> None:
        self._root.mainloop()

    def _build_ui(self) -> None:
        ttk = self._ttk

        outer = ttk.Frame(self._root, padding=12)
        outer.pack(fill="both", expand=True)

        settings_frame = ttk.LabelFrame(outer, text="Instellingen", padding=10)
        settings_frame.pack(fill="x")

        self._add_path_row(
            settings_frame,
            0,
            "Inputmap",
            self._input_var,
            self._choose_input,
        )
        self._add_path_row(
            settings_frame,
            1,
            "Outputmap",
            self._output_var,
            self._choose_output,
        )

        ttk.Label(settings_frame, text="MuScriptor command").grid(
            row=2, column=0, sticky="w", pady=4
        )
        ttk.Entry(settings_frame, textvariable=self._muscriptor_var).grid(
            row=2, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=4
        )

        ttk.Label(settings_frame, text="ffmpeg command").grid(
            row=3, column=0, sticky="w", pady=4
        )
        ttk.Entry(settings_frame, textvariable=self._ffmpeg_var).grid(
            row=3, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=4
        )

        ttk.Label(settings_frame, text="Standaard formaat").grid(
            row=4, column=0, sticky="w", pady=4
        )
        format_box = ttk.Combobox(
            settings_frame,
            textvariable=self._default_format_var,
            values=Converter.VALID_FORMATS,
            state="readonly",
            width=12,
        )
        format_box.grid(row=4, column=1, sticky="w", padx=(8, 0), pady=4)
        format_box.bind("<<ComboboxSelected>>", self._apply_default_format)

        ttk.Button(
            settings_frame,
            text="Instellingen opslaan",
            command=self._save_config,
        ).grid(row=4, column=2, sticky="e", pady=4)

        settings_frame.columnconfigure(1, weight=1)

        files_frame = ttk.LabelFrame(outer, text="MP3-bestanden", padding=10)
        files_frame.pack(fill="both", expand=True, pady=(12, 0))

        toolbar = ttk.Frame(files_frame)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Button(toolbar, text="Vernieuwen", command=self._refresh_files).pack(
            side="left"
        )
        ttk.Button(
            toolbar, text="Geselecteerd -> MIDI",
            command=lambda: self._set_selected_format("midi"),
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            toolbar, text="Geselecteerd -> WAV",
            command=lambda: self._set_selected_format("wav"),
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            toolbar, text="Geselecteerd -> Sheet",
            command=lambda: self._set_selected_format("sheet"),
        ).pack(side="left", padx=(8, 0))

        self._tree = ttk.Treeview(
            files_frame,
            columns=("format",),
            show="tree headings",
            selectmode="extended",
        )
        self._tree.heading("#0", text="Bestand")
        self._tree.heading("format", text="Uitvoer")
        self._tree.column("#0", width=650, stretch=True)
        self._tree.column("format", width=120, anchor="center", stretch=False)

        scrollbar = ttk.Scrollbar(
            files_frame, orient="vertical", command=self._tree.yview
        )
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(12, 0))

        self._convert_button = ttk.Button(
            bottom,
            text="Converteer selectie / alles",
            command=self._start_conversion,
        )
        self._convert_button.pack(side="left")
        ttk.Label(bottom, textvariable=self._status_var).pack(
            side="left", padx=(12, 0)
        )

        ttk.Button(bottom, text="Log", command=self._show_log).pack(side="right")
        self._log_lines: list[str] = []

    def _add_path_row(self, parent, row: int, label: str, variable, command) -> None:
        ttk = self._ttk
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable).grid(
            row=row, column=1, sticky="ew", padx=(8, 8), pady=4
        )
        ttk.Button(parent, text="Kies…", command=command).grid(
            row=row, column=2, sticky="e", pady=4
        )

    def _choose_input(self) -> None:
        selected = self._filedialog.askdirectory(
            initialdir=self._input_var.get() or None
        )
        if selected:
            self._input_var.set(selected)
            self._refresh_files()

    def _choose_output(self) -> None:
        selected = self._filedialog.askdirectory(
            initialdir=self._output_var.get() or None
        )
        if selected:
            self._output_var.set(selected)

    def _refresh_files(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

        input_dir = Path(self._input_var.get()).expanduser()
        default_format = self._default_format_var.get()

        if not input_dir.is_dir():
            self._status_var.set("Inputmap bestaat niet")
            return

        files = sorted(input_dir.glob("*.mp3"))
        for source in files:
            selected_format = self._file_formats.get(source.name, default_format)
            self._file_formats[source.name] = selected_format
            self._tree.insert(
                "",
                "end",
                iid=source.name,
                text=source.name,
                values=(selected_format,),
            )

        self._status_var.set(f"{len(files)} MP3-bestand(en) gevonden")

    def _apply_default_format(self, _event=None) -> None:
        new_format = self._default_format_var.get()
        for item in self._tree.get_children():
            self._file_formats[item] = new_format
            self._tree.set(item, "format", new_format)

    def _set_selected_format(self, output_format: str) -> None:
        selected = self._tree.selection()
        if not selected:
            return
        for item in selected:
            self._file_formats[item] = output_format
            self._tree.set(item, "format", output_format)

    def _current_settings(self) -> AppSettings:
        return AppSettings(
            input_dir=Path(self._input_var.get()).expanduser(),
            output_dir=Path(self._output_var.get()).expanduser(),
            muscriptor_command=self._muscriptor_var.get().strip(),
            ffmpeg_command=self._ffmpeg_var.get().strip(),
            default_format=self._default_format_var.get(),
        )

    def _save_config(self) -> None:
        try:
            self._config_manager.save(self._current_settings())
            self._status_var.set(
                f"Opgeslagen: {self._config_manager.config_path.name}"
            )
        except OSError as exc:
            self._messagebox.showerror("Opslaan mislukt", str(exc))

    def _start_conversion(self) -> None:
        settings = self._current_settings()
        selected_items = list(self._tree.selection())
        items_to_convert = (
            selected_items if selected_items else list(self._tree.get_children())
        )

        jobs = [
            ConversionJob(
                source=settings.input_dir / item,
                output_format=self._file_formats.get(
                    item, settings.default_format
                ),
            )
            for item in items_to_convert
        ]

        if not jobs:
            self._messagebox.showinfo("Geen bestanden", "Geen MP3-bestanden gevonden.")
            return

        self._convert_button.configure(state="disabled")
        self._status_var.set("Conversie bezig…")
        self._log_lines.clear()

        thread = threading.Thread(
            target=self._conversion_worker,
            args=(settings, jobs),
            daemon=True,
        )
        thread.start()

    def _conversion_worker(
        self,
        settings: AppSettings,
        jobs: list[ConversionJob],
    ) -> None:
        converter = Converter(settings)

        def log(message: str) -> None:
            self._log_lines.append(message)
            self._root.after(0, self._status_var.set, message)

        try:
            ok = converter.convert(jobs, on_message=log)
            final = "Alle conversies klaar." if ok else "Klaar met één of meer fouten."
        except Exception as exc:
            final = f"FOUT: {exc}"
            self._log_lines.append(final)

        self._root.after(0, self._finish_conversion, final)

    def _finish_conversion(self, message: str) -> None:
        self._convert_button.configure(state="normal")
        self._status_var.set(message)

    def _show_log(self) -> None:
        window = self._tk.Toplevel(self._root)
        window.title("Conversielog")
        window.geometry("900x500")
        text = self._tk.Text(window, wrap="word")
        text.pack(fill="both", expand=True)
        text.insert("1.0", "\n".join(self._log_lines) or "Nog geen log.")
        text.configure(state="disabled")


class MuscriptorBatchApplication:
    def __init__(self) -> None:
        self._script_path = Path(__file__).resolve()
        self._config_manager = ConfigurationManager(
            self._script_path.with_suffix(".cfg")
        )

    def run(self, argv: list[str] | None = None) -> int:
        args_list = list(sys.argv[1:] if argv is None else argv)
        fallback = self._default_settings()
        saved = self._config_manager.load(fallback)

        if not args_list:
            DesktopApp(saved, self._config_manager).run()
            return 0

        parser = self._create_parser(saved)
        args = parser.parse_args(args_list)
        settings = self._settings_from_args(args)

        if args.save_config:
            self._config_manager.save(settings)
            print(f"Configuratie opgeslagen: {self._config_manager.config_path}")

        overrides = self._parse_overrides(args.file_format)
        jobs = JobResolver(settings.input_dir).resolve(
            args.files,
            args.format,
            overrides,
        )

        if not jobs:
            print(f"Geen MP3-bestanden gevonden in: {settings.input_dir}", file=sys.stderr)
            return 2

        converter = Converter(settings)
        ok = converter.convert(jobs, on_message=print)
        return 0 if ok else 1

    def _default_settings(self) -> AppSettings:
        return AppSettings(
            input_dir=Path(
                "/Volumes/data1/Yandex.Disk.localized/michiele/Muziek/Logic/Bounces"
            ),
            output_dir=Path(
                "/Volumes/data1/Yandex.Disk.localized/michiele/Muziek/Midi bestanden"
            ),
            muscriptor_command="uvx muscriptor",
            ffmpeg_command="ffmpeg",
            default_format="midi",
        )

    def _create_parser(self, saved: AppSettings) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Batch MP3 -> MIDI/WAV/sheet converter using MuScriptor."
        )
        parser.add_argument(
            "-i", "--input-dir",
            type=Path,
            default=saved.input_dir,
            help="Inputmap met MP3-bestanden.",
        )
        parser.add_argument(
            "-o", "--output-dir",
            type=Path,
            default=saved.output_dir,
            help="Outputmap.",
        )
        parser.add_argument(
            "--muscriptor-command",
            default=saved.muscriptor_command,
            help='MuScriptor launcher, bv. "uvx muscriptor" of "muscriptor".',
        )
        parser.add_argument(
            "--ffmpeg-command",
            default=saved.ffmpeg_command,
            help='ffmpeg launcher, standaard "ffmpeg".',
        )
        parser.add_argument(
            "-f", "--format",
            choices=Converter.VALID_FORMATS,
            default=saved.default_format,
            help="Standaard uitvoerformaat voor alle bestanden.",
        )
        parser.add_argument(
            "--files",
            nargs="+",
            help="Expliciete bestanden; relatief aan inputmap of absolute paden.",
        )
        parser.add_argument(
            "--file-format",
            action="append",
            default=[],
            metavar="FILE=FORMAT",
            help=(
                "Per-bestand override, herhaalbaar. "
                'Voorbeeld: --file-format "song.mp3=sheet"'
            ),
        )
        parser.add_argument(
            "--save-config",
            action="store_true",
            help="Sla de effectieve instellingen op in het .cfg-bestand.",
        )
        return parser

    def _settings_from_args(self, args: argparse.Namespace) -> AppSettings:
        return AppSettings(
            input_dir=args.input_dir.expanduser(),
            output_dir=args.output_dir.expanduser(),
            muscriptor_command=args.muscriptor_command,
            ffmpeg_command=args.ffmpeg_command,
            default_format=args.format,
        )

    def _parse_overrides(self, values: list[str]) -> dict[str, str]:
        overrides: dict[str, str] = {}
        for value in values:
            if "=" not in value:
                raise ValueError(
                    f"Ongeldige --file-format '{value}'; gebruik FILE=FORMAT."
                )

            filename, output_format = value.rsplit("=", 1)
            output_format = output_format.lower().strip()
            filename = filename.strip()

            if output_format not in Converter.VALID_FORMATS:
                raise ValueError(
                    f"Ongeldig formaat '{output_format}' voor '{filename}'."
                )
            overrides[filename] = output_format
        return overrides


if __name__ == "__main__":
    raise SystemExit(MuscriptorBatchApplication().run())
