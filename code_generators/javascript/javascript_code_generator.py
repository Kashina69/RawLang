from code_generators.common import parse_rawlang


def generate_javascript_code(english_code: str) -> str:
    statements = parse_rawlang(english_code, "javascript")
    out: list[str] = []
    indent = 0

    def line(txt: str) -> None:
        out.append("    " * indent + txt)

    for st in statements:
        if st.kind == "blank":
            out.append("")
        elif st.kind == "dedent":
            if indent > 0:
                indent -= 1
                out.append("    " * indent + "}")
        elif st.kind == "comment":
            line(f"// {st.text}")
        elif st.kind == "assign":
            line(f"let {st.target} = {st.text};")
        elif st.kind == "print":
            line(f"console.log({st.text});")
        elif st.kind == "function":
            params = ", ".join(st.args or [])
            line(f"function {st.name}({params}) {{")
            indent += 1
        elif st.kind == "return":
            line(f"return {st.text};")
        elif st.kind == "if":
            line(f"if ({st.condition}) {{")
            indent += 1
        elif st.kind == "elif":
            indent = max(0, indent - 1)
            line(f"}} else if ({st.condition}) {{")
            indent += 1
        elif st.kind == "else":
            indent = max(0, indent - 1)
            line("} else {")
            indent += 1
        elif st.kind == "for_range":
            line(f"for (let {st.var} = {st.start}; {st.var} < {st.end}; {st.var}++) {{")
            indent += 1
        elif st.kind == "for_each":
            line(f"for (const {st.var} of {st.iterable}) {{")
            indent += 1
        elif st.kind == "raw":
            out.extend(st.raw_lines or [])
        else:
            line(st.text.rstrip(";") + ";")

    while indent > 0:
        indent -= 1
        out.append("    " * indent + "}")
    return "\n".join(out).rstrip() + "\n"
