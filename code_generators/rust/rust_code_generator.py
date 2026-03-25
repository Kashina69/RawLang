from code_generators.common import parse_rawlang


def generate_rust_code(english_code: str) -> str:
    statements = parse_rawlang(english_code, "rust")
    body: list[str] = []
    indent = 1

    def line(txt: str) -> None:
        body.append("    " * indent + txt)

    for st in statements:
        if st.kind == "blank":
            body.append("")
        elif st.kind == "dedent":
            if indent > 1:
                indent -= 1
                body.append("    " * indent + "}")
        elif st.kind == "comment":
            line(f"// {st.text}")
        elif st.kind == "assign":
            line(f"let mut {st.target} = {st.text};")
        elif st.kind == "print":
            line(f"println!(\"{{:?}}\", {st.text});")
        elif st.kind == "function":
            params = ", ".join(f"{p}: i64" for p in (st.args or []))
            line(f"fn {st.name}({params}) -> i64 {{")
            indent += 1
        elif st.kind == "return":
            line(f"return {st.text};")
        elif st.kind == "if":
            line(f"if {st.condition} {{")
            indent += 1
        elif st.kind == "elif":
            indent = max(1, indent - 1)
            line(f"}} else if {st.condition} {{")
            indent += 1
        elif st.kind == "else":
            indent = max(1, indent - 1)
            line("} else {")
            indent += 1
        elif st.kind == "for_range":
            line(f"for {st.var} in {st.start}..{st.end} {{")
            indent += 1
        elif st.kind == "for_each":
            line(f"for {st.var} in {st.iterable} {{")
            indent += 1
        elif st.kind == "raw":
            body.extend(st.raw_lines or [])
        else:
            line(st.text.rstrip(";") + ";")

    while indent > 1:
        indent -= 1
        body.append("    " * indent + "}")

    out = ["fn main() {"]
    out.extend(body)
    out.append("}")
    return "\n".join(out).rstrip() + "\n"
