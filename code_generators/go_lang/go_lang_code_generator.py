from code_generators.common import parse_rawlang


def generate_golang_code(english_code: str) -> str:
    statements = parse_rawlang(english_code, "golang")
    body: list[str] = []
    indent = 1

    def line(txt: str) -> None:
        body.append("\t" * indent + txt)

    for st in statements:
        if st.kind == "blank":
            body.append("")
        elif st.kind == "dedent":
            if indent > 1:
                indent -= 1
                body.append("\t" * indent + "}")
        elif st.kind == "comment":
            line(f"// {st.text}")
        elif st.kind == "assign":
            line(f"{st.target} := {st.text}")
        elif st.kind == "print":
            line(f"fmt.Println({st.text})")
        elif st.kind == "function":
            params = ", ".join(f"{p} interface{{}}" for p in (st.args or []))
            line(f"func {st.name}({params}) interface{{}} {{")
            indent += 1
        elif st.kind == "return":
            line(f"return {st.text}")
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
            line(f"for {st.var} := {st.start}; {st.var} < {st.end}; {st.var}++ {{")
            indent += 1
        elif st.kind == "for_each":
            line(f"for _, {st.var} := range {st.iterable} {{")
            indent += 1
        elif st.kind == "raw":
            body.extend(st.raw_lines or [])
        else:
            line(st.text)

    while indent > 1:
        indent -= 1
        body.append("\t" * indent + "}")

    out = ["package main", "", 'import "fmt"', "", "func main() {"]
    out.extend(body)
    out.append("}")
    return "\n".join(out).rstrip() + "\n"
