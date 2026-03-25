from code_generators.common import parse_rawlang


def generate_python_code(english_code: str) -> str:
    statements = parse_rawlang(english_code, "python")
    out: list[str] = []
    indent = 0

    for st in statements:
        if st.kind == "blank":
            out.append("")
            continue
        if st.kind == "dedent":
            indent = max(0, indent - 1)
            continue

        if st.kind == "elif" or st.kind == "else":
            indent = max(0, indent - 1)

        prefix = "    " * indent
        if st.kind == "comment":
            out.append(f"{prefix}# {st.text}")
        elif st.kind == "assign":
            out.append(f"{prefix}{st.target} = {st.text}")
        elif st.kind == "print":
            out.append(f"{prefix}print({st.text})")
        elif st.kind == "function":
            params = ", ".join(st.args or [])
            out.append(f"{prefix}def {st.name}({params}):")
            indent += 1
        elif st.kind == "return":
            out.append(f"{prefix}return {st.text}")
        elif st.kind == "if":
            out.append(f"{prefix}if {st.condition}:")
            indent += 1
        elif st.kind == "elif":
            out.append(f"{prefix}elif {st.condition}:")
            indent += 1
        elif st.kind == "else":
            out.append(f"{prefix}else:")
            indent += 1
        elif st.kind == "for_range":
            out.append(f"{prefix}for {st.var} in range({st.start}, {st.end}):")
            indent += 1
        elif st.kind == "for_each":
            out.append(f"{prefix}for {st.var} in {st.iterable}:")
            indent += 1
        elif st.kind == "raw":
            out.extend(st.raw_lines or [])
        else:
            out.append(f"{prefix}{st.text}")

    return "\n".join(out).rstrip() + "\n"
