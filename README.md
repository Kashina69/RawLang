# RawLang

RawLang is a lightweight source-to-source transpiler that converts readable, English-like instructions into code for:

- Python
- JavaScript
- Go
- Rust

It is designed for fast prototyping while still allowing **manual code injection** using fenced code blocks (``` ... ```).

## What is improved in this version

- A shared parser is used for all target languages for consistent behavior.
- The CLI no longer computes every language generator per run (faster conversion path).
- Generators now support a broader set of common language features.
- Added support for manual/real-code blocks inside RawLang files.
- Clear, practical documentation and examples.

## Install / Run

```bash
python main.py <path-to-file.rl>
```

Example:

```bash
python main.py ./main.rl
```

Generated files are written to `generated_code/` using the source file name and target extension.

## Required file header

Every `.rl` file must start with:

```rawlang
language should be python
```

Supported values: `python`, `javascript`, `golang`, `rust`.

---

## RawLang syntax guide

### 1) Variables

```rawlang
make score = 10
make name = "RawLang"
assign 20 to score
```

### 2) Lists, sets, tuples, objects

```rawlang
make list nums = 1 2 3 4
make set tags = "dev" "tools"
make tuple pair = 10 20
make object user = name "Raw" age 19
```

### 3) Print

```rawlang
print "hello"
prints score
```

### 4) Functions + return

```rawlang
create function add with parameters x, y which
print x + y
return x + y
.
```

Use `.` to close the current block in indentation-sensitive output (especially Python generation).

### 5) Function calls

```rawlang
call add with arguments 5, 6
```

### 6) Conditions

```rawlang
check if score > 10
print "high"
otherwise if score == 10
print "equal"
otherwise
print "low"
.
```

### 7) Loops

Range loop:

```rawlang
loop i from 0 to 10
print i
.
```

For-each loop:

```rawlang
loop for item in nums
print item
.
```

---

## Manual code blocks (real code)

You can embed direct target-language code:

````rawlang
```python
print("manual python block")
```
````

Rules:

- ` ```python `, ` ```javascript `, ` ```golang `, ` ```rust ` only pass through when the selected target matches.
- Plain ` ``` ` (no language tag), ` ```code `, ` ```real code `, or ` ```manual ` passes through for any target.

This gives you a safe fallback for advanced cases the parser doesn't yet cover.

---

## End-to-end example

Input (`example.rl`):

````rawlang
language should be javascript
make value = 3
create function show with parameters x which
print x
.
call show with arguments value
```javascript
console.log("custom JS tail");
```
````

Output (`generated_code/example.js`) will include both generated JS and your manual block.

---

## Project structure

- `main.py` — CLI entry point and file orchestration.
- `code_generators/common.py` — shared parser and normalized statements.
- `code_generators/python/python_code_generator.py` — Python emitter.
- `code_generators/javascript/javascript_code_generator.py` — JavaScript emitter.
- `code_generators/go_lang/go_lang_code_generator.py` — Go emitter.
- `code_generators/rust/rust_code_generator.py` — Rust emitter.

## Notes / limitations

- Rust and Go output is best-effort for generic typing scenarios.
- For highly language-specific constructs, use manual fenced blocks.
- Keep expressions explicit in RawLang (e.g., `x + y`, `name == "a"`) for predictable conversion.

## License

MIT
