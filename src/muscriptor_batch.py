#!/usr/bin/env python3
"""
File     : muscriptor_batch.py
Version  : 0.2.2
ChatID   : 6F3A9C21
Purpose  : Cross-platform MuScriptor MP3 batch converter with CLI and desktop UI.

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

VERSION = "0.2.2"
RELEASE_CHAT_ID = "6F3A9C21"

import argparse
import configparser
import shlex
import subprocess
import sys
import threading

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


DEFAULT_INPUT_DIR = Path(
    "/Volumes/data1/Yandex.Disk.localized/"
    "michiele/Muziek/Logic/Bounces"
)

DEFAULT_OUTPUT_DIR = Path(
    "/Volumes/data1/Yandex.Disk.localized/"
    "michiele/Muziek/Midi bestanden"
)

DEFAULT_MUSCRIPTOR_COMMAND = "muscriptor"
DEFAULT_FFMPEG_COMMAND = "ffmpeg"
DEFAULT_FORMAT = "midi"

VALID_FORMATS = ("midi", "wav", "sheet")


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    """Immutable release identification."""

    version: str
    chat_id: str

    def display_text(self) -> str:
        """Return human-readable release identification."""
        return f"Version {self.version} · ChatID {self.chat_id}"


@dataclass(slots=True)
class AppSettings:
    """Application configuration."""

    input_dir: Path = DEFAULT_INPUT_DIR
    output_dir: Path = DEFAULT_OUTPUT_DIR
    muscriptor_command: str = DEFAULT_MUSCRIPTOR_COMMAND
    ffmpeg_command: str = DEFAULT_FFMPEG_COMMAND
    default_format: str = DEFAULT_FORMAT


@dataclass(frozen=True, slots=True)
class ConversionJob:
    """One input file and its requested output format."""

    source: Path
    output_format: str


class ConfigurationManager:
    """Load and save application configuration."""

    SECTION = "settings"

    def __init__(self, config_path: Path) -> None:
        self._config_path = Path(config_path)

    @property
    def config_path(self) -> Path:
        return self._config_path

    def load(
        self,
        fallback: AppSettings | None = None,
    ) -> AppSettings:
        settings = fallback or AppSettings()

        if not self._config_path.exists():
            return settings

        parser = configparser.ConfigParser()
        parser.read(self._config_path, encoding="utf-8")

        if not parser.has_section(self.SECTION):
            return settings

        section = parser[self.SECTION]

        return AppSettings(
            input_dir=Path(
                section.get(
                    "input_dir",
                    str(settings.input_dir),
                )
            ).expanduser(),
            output_dir=Path(
                section.get(
                    "output_dir",
                    str(settings.output_dir),
                )
            ).expanduser(),
            muscriptor_command=section.get(
                "muscriptor_command",
                settings.muscriptor_command,
            ),
            ffmpeg_command=section.get(
                "ffmpeg_command",
                settings.ffmpeg_command,
            ),
            default_format=section.get(
                "default_format",
                settings.default_format,
            ),
        )

    def save(self, settings: AppSettings) -> None:
        parser = configparser.ConfigParser()

        parser[self.SECTION] = {
            "input_dir": str(settings.input_dir),
            "output_dir": str(settings.output_dir),
            "muscriptor_command": settings.muscriptor_command,
            "ffmpeg_command": settings.ffmpeg_command,
            "default_format": settings.default_format,
        }

        self._config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._config_path.open(
            "w",
            encoding="utf-8",
        ) as handle:
            parser.write(handle)


class CommandBuilder:
    """Build external commands without invoking a shell."""

    def __init__(
        self,
        muscriptor_command: str,
        ffmpeg_command: str,
    ) -> None:
        self._muscriptor_command = muscriptor_command
        self._ffmpeg_command = ffmpeg_command

    @staticmethod
    def _split_command(command: str) -> list[str]:
        return shlex.split(command)

    def build_midi(
        self,
        source: Path,
        destination: Path,
    ) -> list[str]:
        return [
            *self._split_command(self._muscriptor_command),
            "transcribe",
            str(source),
            "--format",
            "midi",
            "--output",
            str(destination),
        ]

    def build_sheet(
        self,
        source: Path,
        output_directory: Path,
    ) -> list[str]:
        return [
            *self._split_command(self._muscriptor_command),
            "transcribe",
            str(source),
            "--format",
            "sheets",
            "--output",
            str(output_directory),
        ]

    def build_wav(
        self,
        source: Path,
        destination: Path,
    ) -> list[str]:
        return [
            *self._split_command(self._ffmpeg_command),
            "-y",
            "-i",
            str(source),
            "-c:a",
            "pcm_s16le",
            str(destination),
        ]


class JobResolver:
    """Resolve CLI/UI file selections into conversion jobs."""

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings

    def resolve(
        self,
        explicit_files: Sequence[str | Path] | None = None,
        default_format: str | None = None,
        per_file_formats: dict[str, str] | None = None,
    ) -> list[ConversionJob]:
        requested_format = (
            default_format
            or self._settings.default_format
        )

        self._validate_format(requested_format)

        overrides = per_file_formats or {}

        if explicit_files:
            files = [
                self._resolve_explicit_file(file_name)
                for file_name in explicit_files
            ]
        else:
            files = self._find_mp3_files()

        jobs: list[ConversionJob] = []

        for source in files:
            output_format = self._lookup_override(
                source,
                overrides,
                requested_format,
            )

            self._validate_format(output_format)

            jobs.append(
                ConversionJob(
                    source=source,
                    output_format=output_format,
                )
            )

        return jobs

    def _resolve_explicit_file(
        self,
        file_name: str | Path,
    ) -> Path:
        source = Path(file_name).expanduser()

        if not source.is_absolute():
            source = self._settings.input_dir / source

        return source

    def _find_mp3_files(self) -> list[Path]:
        input_dir = self._settings.input_dir

        if not input_dir.exists():
            return []

        return sorted(
            path
            for path in input_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".mp3"
        )

    @staticmethod
    def _lookup_override(
        source: Path,
        overrides: dict[str, str],
        fallback: str,
    ) -> str:
        candidates = (
            str(source),
            source.name,
            source.stem,
        )

        for candidate in candidates:
            if candidate in overrides:
                return overrides[candidate]

        return fallback

    @staticmethod
    def _validate_format(output_format: str) -> None:
        if output_format not in VALID_FORMATS:
            raise ValueError(
                f"Onbekend uitvoerformaat: {output_format}"
            )


class Converter:
    """Execute MuScriptor/ffmpeg conversion jobs."""

    VALID_FORMATS = VALID_FORMATS

    def __init__(
        self,
        settings: AppSettings,
        runner: Callable | None = None,
        process_factory: Callable | None = None,
    ) -> None:
        self._settings = settings

        self._builder = CommandBuilder(
            settings.muscriptor_command,
            settings.ffmpeg_command,
        )

        # runner remains supported for the original unit tests.
        self._runner = runner

        # Popen-style factory is used for live streaming.
        self._process_factory = (
            process_factory
            or subprocess.Popen
        )

    def convert(
        self,
        jobs: Sequence[ConversionJob],
        on_message: Callable[[str], None] | None = None,
    ) -> bool:
        """Convert all jobs and return True only when all succeed."""

        self._settings.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        all_successful = True

        for job in jobs:
            try:
                self._validate_job(job)

                command, expected_output = (
                    self._build_job_command(job)
                )

                self._emit(
                    on_message,
                    (
                        f"Start: {job.source.name} "
                        f"-> {job.output_format}"
                    ),
                )

                self._emit(
                    on_message,
                    "Commando: "
                    + shlex.join(command),
                )

                self._execute(
                    command,
                    on_message,
                )

                if (
                    expected_output is not None
                    and not expected_output.exists()
                ):
                    raise RuntimeError(
                        "Proces eindigde zonder verwachte "
                        f"uitvoer: {expected_output}"
                    )

                self._emit(
                    on_message,
                    f"Klaar: {job.source.name}",
                )

            except Exception as exc:
                all_successful = False

                self._emit(
                    on_message,
                    (
                        f"FOUT: {job.source.name}: "
                        f"{exc}"
                    ),
                )

        return all_successful

    def _execute(
        self,
        command: list[str],
        on_message: Callable[[str], None] | None,
    ) -> None:
        """
        Execute one external command.

        When an old-style injected runner is supplied, retain
        compatibility with the original tests.

        Otherwise use Popen and stream stdout/stderr line-by-line
        to the application callback.
        """

        if self._runner is not None:
            self._runner(
                command,
                check=True,
            )
            return

        process = self._process_factory(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        if process.stdout is not None:
            for raw_line in process.stdout:
                line = raw_line.rstrip("\r\n")

                if line.strip():
                    self._emit(
                        on_message,
                        line,
                    )

        return_code = process.wait()

        if return_code != 0:
            raise subprocess.CalledProcessError(
                return_code,
                command,
            )

    def _validate_job(
        self,
        job: ConversionJob,
    ) -> None:
        if job.output_format not in self.VALID_FORMATS:
            raise ValueError(
                f"Onbekend uitvoerformaat: "
                f"{job.output_format}"
            )

        if not job.source.exists():
            raise FileNotFoundError(
                f"Bronbestand bestaat niet: "
                f"{job.source}"
            )

    def _build_job_command(
        self,
        job: ConversionJob,
    ) -> tuple[list[str], Path | None]:
        output_dir = self._settings.output_dir

        if job.output_format == "midi":
            destination = (
                output_dir
                / f"{job.source.stem}.mid"
            )

            return (
                self._builder.build_midi(
                    job.source,
                    destination,
                ),
                destination,
            )

        if job.output_format == "wav":
            destination = (
                output_dir
                / f"{job.source.stem}.wav"
            )

            return (
                self._builder.build_wav(
                    job.source,
                    destination,
                ),
                destination,
            )

        if job.output_format == "sheet":
            sheet_dir = (
                output_dir
                / job.source.stem
            )

            sheet_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            expected = (
                sheet_dir
                / "score.mid"
            )

            return (
                self._builder.build_sheet(
                    job.source,
                    sheet_dir,
                ),
                expected,
            )

        raise ValueError(
            f"Onbekend uitvoerformaat: "
            f"{job.output_format}"
        )

    @staticmethod
    def _emit(
        callback: Callable[[str], None] | None,
        message: str,
    ) -> None:
        if callback is not None:
            callback(message)


class DesktopApp:
    """Tkinter desktop interface."""

    def __init__(
        self,
        settings: AppSettings,
        config_manager: ConfigurationManager,
    ) -> None:
        import tkinter as tk
        from tkinter import filedialog
        from tkinter import messagebox
        from tkinter import ttk

        self._tk = tk
        self._ttk = ttk
        self._filedialog = filedialog
        self._messagebox = messagebox

        self._settings = settings
        self._config_manager = config_manager

        self._root = tk.Tk()

        self._root.title(
            "MuScriptor MP3 converter — "
            f"{self.build_release_text()}"
        )

        self._root.geometry("980x760")
        self._root.minsize(860, 620)

        self._input_var = tk.StringVar(
            value=str(settings.input_dir)
        )

        self._output_var = tk.StringVar(
            value=str(settings.output_dir)
        )

        self._muscriptor_var = tk.StringVar(
            value=settings.muscriptor_command
        )

        self._ffmpeg_var = tk.StringVar(
            value=settings.ffmpeg_command
        )

        self._default_format_var = tk.StringVar(
            value=settings.default_format
        )

        self._status_var = tk.StringVar(
            value="Gereed"
        )

        self._selected_files: list[Path] = []
        self._file_formats: dict[str, str] = {}
        self._log_lines: list[str] = []

        self._build_ui()

    @staticmethod
    def build_release_text() -> str:
        """Return release identity displayed by the UI."""

        return ReleaseInfo(
            version=VERSION,
            chat_id=RELEASE_CHAT_ID,
        ).display_text()

    def run(self) -> None:
        self._root.mainloop()

    def _build_ui(self) -> None:
        ttk = self._ttk

        outer = ttk.Frame(
            self._root,
            padding=12,
        )

        outer.pack(
            fill="both",
            expand=True,
        )

        # Release information is deliberately visible in the
        # application itself, not only in the window title.
        release_label = ttk.Label(
            outer,
            text=self.build_release_text(),
        )

        release_label.pack(
            anchor="e",
            pady=(0, 8),
        )

        settings_frame = ttk.LabelFrame(
            outer,
            text="Instellingen",
            padding=10,
        )

        settings_frame.pack(
            fill="x",
        )

        self._build_path_row(
            settings_frame,
            row=0,
            label="Inputmap",
            variable=self._input_var,
            command=self._choose_input_dir,
        )

        self._build_path_row(
            settings_frame,
            row=1,
            label="Outputmap",
            variable=self._output_var,
            command=self._choose_output_dir,
        )

        ttk.Label(
            settings_frame,
            text="MuScriptor commando",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        ttk.Entry(
            settings_frame,
            textvariable=self._muscriptor_var,
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            pady=4,
        )

        ttk.Label(
            settings_frame,
            text="ffmpeg commando",
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        ttk.Entry(
            settings_frame,
            textvariable=self._ffmpeg_var,
        ).grid(
            row=3,
            column=1,
            sticky="ew",
            pady=4,
        )

        ttk.Label(
            settings_frame,
            text="Standaard formaat",
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        format_box = ttk.Combobox(
            settings_frame,
            textvariable=self._default_format_var,
            values=VALID_FORMATS,
            state="readonly",
            width=12,
        )

        format_box.grid(
            row=4,
            column=1,
            sticky="w",
            pady=4,
        )

        settings_frame.columnconfigure(
            1,
            weight=1,
        )

        action_frame = ttk.Frame(
            outer,
        )

        action_frame.pack(
            fill="x",
            pady=(12, 0),
        )

        ttk.Button(
            action_frame,
            text="Bestanden kiezen",
            command=self._choose_files,
        ).pack(
            side="left",
        )

        ttk.Button(
            action_frame,
            text="MP3-bestanden uit inputmap",
            command=self._load_input_files,
        ).pack(
            side="left",
            padx=(8, 0),
        )

        ttk.Button(
            action_frame,
            text="Configuratie opslaan",
            command=self._save_configuration,
        ).pack(
            side="right",
        )

        files_frame = ttk.LabelFrame(
            outer,
            text="Bestanden",
            padding=8,
        )

        files_frame.pack(
            fill="both",
            expand=True,
            pady=(12, 0),
        )

        columns = (
            "file",
            "format",
        )

        self._tree = ttk.Treeview(
            files_frame,
            columns=columns,
            show="headings",
            selectmode="extended",
        )

        self._tree.heading(
            "file",
            text="Bestand",
        )

        self._tree.heading(
            "format",
            text="Uitvoer",
        )

        self._tree.column(
            "file",
            width=650,
            anchor="w",
        )

        self._tree.column(
            "format",
            width=100,
            anchor="center",
        )

        scrollbar = ttk.Scrollbar(
            files_frame,
            orient="vertical",
            command=self._tree.yview,
        )

        self._tree.configure(
            yscrollcommand=scrollbar.set,
        )

        self._tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        per_file_frame = ttk.Frame(
            outer,
        )

        per_file_frame.pack(
            fill="x",
            pady=(8, 0),
        )

        ttk.Label(
            per_file_frame,
            text="Formaat geselecteerde bestanden:",
        ).pack(
            side="left",
        )

        for output_format in VALID_FORMATS:
            ttk.Button(
                per_file_frame,
                text=output_format,
                command=lambda fmt=output_format:
                    self._set_selected_format(fmt),
            ).pack(
                side="left",
                padx=(6, 0),
            )

        console_frame = ttk.LabelFrame(
            outer,
            text="Live conversie-output",
            padding=8,
        )

        console_frame.pack(
            fill="both",
            expand=True,
            pady=(12, 0),
        )

        self._console = self._tk.Text(
            console_frame,
            height=12,
            wrap="word",
            state="disabled",
        )

        console_scrollbar = ttk.Scrollbar(
            console_frame,
            orient="vertical",
            command=self._console.yview,
        )

        self._console.configure(
            yscrollcommand=console_scrollbar.set,
        )

        self._console.pack(
            side="left",
            fill="both",
            expand=True,
        )

        console_scrollbar.pack(
            side="right",
            fill="y",
        )

        bottom = ttk.Frame(
            outer,
        )

        bottom.pack(
            fill="x",
            pady=(12, 0),
        )

        ttk.Label(
            bottom,
            textvariable=self._status_var,
        ).pack(
            side="left",
            fill="x",
            expand=True,
        )

        self._convert_button = ttk.Button(
            bottom,
            text="Converteren",
            command=self._start_conversion,
        )

        self._convert_button.pack(
            side="right",
        )

    def _build_path_row(
        self,
        parent,
        row: int,
        label: str,
        variable,
        command: Callable[[], None],
    ) -> None:
        ttk = self._ttk

        ttk.Label(
            parent,
            text=label,
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=4,
        )

        ttk.Entry(
            parent,
            textvariable=variable,
        ).grid(
            row=row,
            column=1,
            sticky="ew",
            pady=4,
        )

        ttk.Button(
            parent,
            text="Kies…",
            command=command,
        ).grid(
            row=row,
            column=2,
            padx=(8, 0),
            pady=4,
        )

    def _choose_input_dir(self) -> None:
        selected = self._filedialog.askdirectory(
            initialdir=self._input_var.get(),
        )

        if selected:
            self._input_var.set(selected)

    def _choose_output_dir(self) -> None:
        selected = self._filedialog.askdirectory(
            initialdir=self._output_var.get(),
        )

        if selected:
            self._output_var.set(selected)

    def _choose_files(self) -> None:
        selected = self._filedialog.askopenfilenames(
            initialdir=self._input_var.get(),
            filetypes=[
                ("MP3 files", "*.mp3"),
                ("All files", "*.*"),
            ],
        )

        if not selected:
            return

        self._selected_files = [
            Path(file_name)
            for file_name in selected
        ]

        self._refresh_tree()

    def _load_input_files(self) -> None:
        input_dir = Path(
            self._input_var.get()
        ).expanduser()

        if not input_dir.exists():
            self._messagebox.showerror(
                "Fout",
                f"Inputmap bestaat niet:\n{input_dir}",
            )
            return

        self._selected_files = sorted(
            path
            for path in input_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".mp3"
        )

        self._refresh_tree()

    def _refresh_tree(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

        default_format = (
            self._default_format_var.get()
            or DEFAULT_FORMAT
        )

        for source in self._selected_files:
            output_format = self._file_formats.get(
                str(source),
                default_format,
            )

            self._tree.insert(
                "",
                "end",
                iid=str(source),
                values=(
                    source.name,
                    output_format,
                ),
            )

    def _set_selected_format(
        self,
        output_format: str,
    ) -> None:
        if output_format not in VALID_FORMATS:
            return

        for item in self._tree.selection():
            self._file_formats[item] = (
                output_format
            )

            values = list(
                self._tree.item(
                    item,
                    "values",
                )
            )

            if len(values) >= 2:
                values[1] = output_format

            self._tree.item(
                item,
                values=values,
            )

    def _current_settings(self) -> AppSettings:
        return AppSettings(
            input_dir=Path(
                self._input_var.get()
            ).expanduser(),
            output_dir=Path(
                self._output_var.get()
            ).expanduser(),
            muscriptor_command=(
                self._muscriptor_var.get().strip()
                or DEFAULT_MUSCRIPTOR_COMMAND
            ),
            ffmpeg_command=(
                self._ffmpeg_var.get().strip()
                or DEFAULT_FFMPEG_COMMAND
            ),
            default_format=(
                self._default_format_var.get()
                or DEFAULT_FORMAT
            ),
        )

    def _save_configuration(self) -> None:
        settings = self._current_settings()

        try:
            self._config_manager.save(
                settings
            )

        except Exception as exc:
            self._messagebox.showerror(
                "Configuratiefout",
                str(exc),
            )
            return

        self._status_var.set(
            "Configuratie opgeslagen: "
            f"{self._config_manager.config_path}"
        )

    def _start_conversion(self) -> None:
        settings = self._current_settings()

        if not self._selected_files:
            resolver = JobResolver(settings)

            jobs = resolver.resolve(
                default_format=settings.default_format,
            )

        else:
            resolver = JobResolver(settings)

            jobs = resolver.resolve(
                explicit_files=self._selected_files,
                default_format=settings.default_format,
                per_file_formats=self._file_formats,
            )

        if not jobs:
            self._messagebox.showinfo(
                "Geen bestanden",
                "Geen MP3-bestanden gevonden "
                "om te converteren.",
            )
            return

        self._convert_button.configure(
            state="disabled",
        )

        self._status_var.set(
            "Conversie bezig…"
        )

        self._log_lines.clear()

        self._console.configure(
            state="normal",
        )

        self._console.delete(
            "1.0",
            "end",
        )

        self._console.configure(
            state="disabled",
        )

        thread = threading.Thread(
            target=self._conversion_worker,
            args=(
                settings,
                jobs,
            ),
            daemon=True,
        )

        thread.start()

    def _conversion_worker(
        self,
        settings: AppSettings,
        jobs: Sequence[ConversionJob],
    ) -> None:
        converter = Converter(
            settings
        )

        def log(message: str) -> None:
            self._log_lines.append(
                message
            )

            self._root.after(
                0,
                self._append_console_line,
                message,
            )

            self._root.after(
                0,
                self._status_var.set,
                message,
            )

        success = converter.convert(
            jobs,
            on_message=log,
        )

        if success:
            final_message = (
                f"Klaar. {len(jobs)} "
                "bestand(en) verwerkt."
            )
        else:
            final_message = (
                "Conversie voltooid met fouten. "
                "Bekijk de live output."
            )

        self._root.after(
            0,
            self._finish_conversion,
            final_message,
        )

    def _append_console_line(
        self,
        message: str,
    ) -> None:
        self._console.configure(
            state="normal",
        )

        self._console.insert(
            "end",
            message + "\n",
        )

        self._console.see(
            "end"
        )

        self._console.configure(
            state="disabled",
        )

    def _finish_conversion(
        self,
        message: str,
    ) -> None:
        self._status_var.set(
            message
        )

        self._convert_button.configure(
            state="normal",
        )


class Application:
    """CLI/GUI application coordinator."""

    def __init__(
        self,
        config_path: Path | None = None,
    ) -> None:
        script_path = Path(__file__).resolve()

        self._config_path = (
            config_path
            if config_path is not None
            else script_path.with_suffix(".cfg")
        )

        self._config_manager = (
            ConfigurationManager(
                self._config_path
            )
        )

    @staticmethod
    def build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description=(
                "Batch MP3 -> MIDI/WAV/sheet "
                "converter using MuScriptor."
            )
        )

        parser.add_argument(
            "--version",
            action="version",
            version=(
                f"%(prog)s Version {VERSION} · "
                f"ChatID {RELEASE_CHAT_ID}"
            ),
        )

        parser.add_argument(
            "-i",
            "--input-dir",
            type=Path,
            help="Inputmap met MP3-bestanden.",
        )

        parser.add_argument(
            "-o",
            "--output-dir",
            type=Path,
            help="Outputmap.",
        )

        parser.add_argument(
            "--muscriptor-command",
            help=(
                "MuScriptor executable/command, "
                "bijvoorbeeld 'muscriptor' of "
                "'uvx muscriptor'."
            ),
        )

        parser.add_argument(
            "--ffmpeg-command",
            help=(
                "ffmpeg executable/command."
            ),
        )

        parser.add_argument(
            "-f",
            "--format",
            choices=VALID_FORMATS,
            help="Standaard uitvoerformaat.",
        )

        parser.add_argument(
            "--files",
            nargs="+",
            help=(
                "Expliciete bestanden om te "
                "converteren. Relatieve paden "
                "worden tegen de inputmap opgelost."
            ),
        )

        parser.add_argument(
            "--file-format",
            action="append",
            default=[],
            metavar="FILE=FORMAT",
            help=(
                "Formaat per bestand. "
                "Mag meerdere keren worden gebruikt."
            ),
        )

        parser.add_argument(
            "--save-config",
            action="store_true",
            help=(
                "Sla de resulterende instellingen "
                "op in het .cfg-bestand."
            ),
        )

        return parser

    def run(
        self,
        argv: Sequence[str] | None = None,
    ) -> int:
        arguments = list(
            sys.argv[1:]
            if argv is None
            else argv
        )

        stored_settings = (
            self._config_manager.load(
                AppSettings()
            )
        )

        # No command-line options:
        # start the desktop application.
        if not arguments:
            DesktopApp(
                stored_settings,
                self._config_manager,
            ).run()

            return 0

        parser = self.build_parser()
        args = parser.parse_args(
            arguments
        )

        settings = AppSettings(
            input_dir=(
                args.input_dir
                if args.input_dir is not None
                else stored_settings.input_dir
            ),
            output_dir=(
                args.output_dir
                if args.output_dir is not None
                else stored_settings.output_dir
            ),
            muscriptor_command=(
                args.muscriptor_command
                if args.muscriptor_command
                else stored_settings.muscriptor_command
            ),
            ffmpeg_command=(
                args.ffmpeg_command
                if args.ffmpeg_command
                else stored_settings.ffmpeg_command
            ),
            default_format=(
                args.format
                if args.format
                else stored_settings.default_format
            ),
        )

        if args.save_config:
            self._config_manager.save(
                settings
            )

        try:
            per_file_formats = (
                self._parse_file_formats(
                    args.file_format
                )
            )

            resolver = JobResolver(
                settings
            )

            jobs = resolver.resolve(
                explicit_files=args.files,
                default_format=settings.default_format,
                per_file_formats=per_file_formats,
            )

        except (
            ValueError,
            OSError,
        ) as exc:
            print(
                f"FOUT: {exc}",
                file=sys.stderr,
            )

            return 2

        if not jobs:
            print(
                "Geen MP3-bestanden gevonden.",
                file=sys.stderr,
            )

            return 1

        converter = Converter(
            settings
        )

        success = converter.convert(
            jobs,
            on_message=print,
        )

        return 0 if success else 1

    @staticmethod
    def _parse_file_formats(
        values: Sequence[str],
    ) -> dict[str, str]:
        result: dict[str, str] = {}

        for value in values:
            if "=" not in value:
                raise ValueError(
                    "--file-format verwacht "
                    "FILE=FORMAT"
                )

            file_name, output_format = (
                value.rsplit(
                    "=",
                    1,
                )
            )

            file_name = file_name.strip()
            output_format = (
                output_format.strip().lower()
            )

            if not file_name:
                raise ValueError(
                    "Bestandsnaam ontbreekt in "
                    "--file-format."
                )

            if output_format not in VALID_FORMATS:
                raise ValueError(
                    "Ongeldig formaat voor "
                    f"{file_name}: "
                    f"{output_format}"
                )

            result[file_name] = (
                output_format
            )

        return result


def main(
    argv: Sequence[str] | None = None,
) -> int:
    """Application entry point."""

    application = Application()

    return application.run(
        argv
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )