import re
from dataclasses import dataclass
from typing import List, Optional


BLOCK_STARTERS = ("if", "elif", "else", "for", "while", "function")


@dataclass
class Statement:
    kind: str
    text: str = ""
    condition: str = ""
    name: str = ""
    args: List[str] | None = None
    target: str = ""
    start: str = ""
    end: str = ""
    iterable: str = ""
    var: str = ""
    raw_lines: List[str] | None = None


def split_csv(raw: str) -> List[str]:
    cleaned = raw.replace(" and ", ", ")
    return [item.strip() for item in cleaned.split(",") if item.strip()]


def normalize_value(token: str) -> str:
    token = token.strip()
    if token.lower() in {"true", "false", "none", "null"}:
        return {"none": "None", "null": "None"}.get(token.lower(), token.lower().capitalize())
    if re.fullmatch(r"-?\d+(\.\d+)?", token):
        return token
    if token.startswith(('"', "'")) and token.endswith(('"', "'")):
        return token
    return token


def _extract_params(rest: str) -> List[str]:
    if "with parameters" in rest:
        raw = rest.split("with parameters", 1)[1]
    elif "with parameter" in rest:
        raw = rest.split("with parameter", 1)[1]
    elif "with parms" in rest:
        raw = rest.split("with parms", 1)[1]
    else:
        return []
    raw = raw.replace("which", "").strip()
    return split_csv(raw)


def parse_rawlang(english_code: str, language: str) -> List[Statement]:
    statements: List[Statement] = []
    lines = english_code.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        if not stripped:
            statements.append(Statement(kind="blank"))
            i += 1
            continue

        if stripped == ".":
            statements.append(Statement(kind="dedent"))
            i += 1
            continue

        if stripped.startswith("```"):
            fence = stripped[3:].strip().lower()
            raw_lines: List[str] = []
            i += 1
            while i < len(lines):
                if lines[i].strip() == "```":
                    break
                raw_lines.append(lines[i])
                i += 1
            include = not fence or fence in {"real code", "code", language, "manual"}
            if include:
                statements.append(Statement(kind="raw", raw_lines=raw_lines))
            i += 1
            continue

        lower = stripped.lower()

        if lower.startswith("#") or lower.startswith("//"):
            statements.append(Statement(kind="comment", text=stripped.lstrip("#/ ")))
            i += 1
            continue

        if lower.startswith("make list ") or lower.startswith("make array ") or lower.startswith("make arr ") or lower.startswith("make lst "):
            rest = stripped.split(maxsplit=2)[2]
            name, values = rest.split("=", 1)
            vals = [normalize_value(v) for v in values.split()]
            statements.append(Statement(kind="assign", target=name.strip(), text="[" + ", ".join(vals) + "]"))
            i += 1
            continue

        if lower.startswith("make set "):
            rest = stripped.split(maxsplit=2)[2]
            name, values = rest.split("=", 1)
            vals = [normalize_value(v) for v in values.split()]
            statements.append(Statement(kind="assign", target=name.strip(), text="{" + ", ".join(vals) + "}"))
            i += 1
            continue

        if lower.startswith("make tuple "):
            rest = stripped.split(maxsplit=2)[2]
            name, values = rest.split("=", 1)
            vals = [normalize_value(v) for v in values.split()]
            trailing = "," if len(vals) == 1 else ""
            statements.append(Statement(kind="assign", target=name.strip(), text="(" + ", ".join(vals) + trailing + ")"))
            i += 1
            continue

        if lower.startswith("make object ") or lower.startswith("make dict ") or lower.startswith("make dictionary "):
            rest = stripped.split(maxsplit=2)[2]
            name, values = rest.split("=", 1)
            parts = values.split()
            kv = []
            for idx in range(0, len(parts) - 1, 2):
                k = parts[idx]
                v = normalize_value(parts[idx + 1])
                kv.append(f'"{k}": {v}')
            statements.append(Statement(kind="assign", target=name.strip(), text="{" + ", ".join(kv) + "}"))
            i += 1
            continue

        if lower.startswith("make ") and "=" in stripped:
            rest = stripped[5:]
            chunks = re.split(r"\s+(?=[A-Za-z_]\w*\s*=)", rest)
            for chunk in chunks:
                if "=" in chunk:
                    target, expr = chunk.split("=", 1)
                    statements.append(Statement(kind="assign", target=target.strip(), text=expr.strip()))
            i += 1
            continue

        if lower.startswith("assign ") and " to " in lower:
            after = stripped[7:]
            expr, target = re.split(r"\bto\b", after, maxsplit=1, flags=re.IGNORECASE)
            target = target.replace("variable", "").replace("as", "").strip()
            statements.append(Statement(kind="assign", target=target, text=expr.strip()))
            i += 1
            continue

        if lower.startswith("print ") or lower.startswith("prints "):
            text = stripped.split(maxsplit=1)[1]
            statements.append(Statement(kind="print", text=text))
            i += 1
            continue

        if lower.startswith("create function ") or lower.startswith("create func ") or lower.startswith("create fun "):
            name = stripped.split()[2]
            params = _extract_params(lower)
            statements.append(Statement(kind="function", name=name, args=params))
            i += 1
            continue

        if lower.startswith("return "):
            statements.append(Statement(kind="return", text=stripped[7:]))
            i += 1
            continue

        if lower.startswith("call "):
            if "with arguments" in lower:
                name = stripped.split()[1]
                args = split_csv(stripped.lower().split("with arguments", 1)[1])
                statements.append(Statement(kind="expr", text=f"{name}({', '.join(args)})"))
            else:
                statements.append(Statement(kind="expr", text=stripped[5:]))
            i += 1
            continue

        if lower.startswith("check if "):
            statements.append(Statement(kind="if", condition=stripped[9:]))
            i += 1
            continue

        if lower.startswith("otherwise check if ") or lower.startswith("otherwise if "):
            cond = re.sub(r"^otherwise\s+(check\s+)?if\s+", "", stripped, flags=re.IGNORECASE)
            statements.append(Statement(kind="elif", condition=cond))
            i += 1
            continue

        if lower == "otherwise" or lower == "else":
            statements.append(Statement(kind="else"))
            i += 1
            continue

        if lower.startswith("loop ") and " from " in lower and " to " in lower:
            m = re.match(r"loop\s+([A-Za-z_]\w*)?\s*from\s+(.+?)\s+to\s+(.+)$", stripped, flags=re.IGNORECASE)
            if m:
                var = m.group(1) or "i"
                statements.append(Statement(kind="for_range", var=var, start=m.group(2).strip(), end=m.group(3).strip()))
                i += 1
                continue

        if lower.startswith("loop for ") and " in " in lower:
            m = re.match(r"loop\s+for\s+([A-Za-z_]\w*)\s+in\s+(.+)$", stripped, flags=re.IGNORECASE)
            if m:
                statements.append(Statement(kind="for_each", var=m.group(1), iterable=m.group(2).strip()))
                i += 1
                continue

        statements.append(Statement(kind="expr", text=stripped))
        i += 1

    return statements
